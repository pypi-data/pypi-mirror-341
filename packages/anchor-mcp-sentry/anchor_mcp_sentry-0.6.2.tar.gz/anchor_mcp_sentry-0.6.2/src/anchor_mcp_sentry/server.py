import asyncio
import json
from dataclasses import dataclass
from typing import Any, Dict
from urllib.parse import urlparse

import click
import httpx
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.shared.exceptions import McpError
import mcp.server.stdio

SENTRY_API_BASE = "https://sentry.io/api/0/"
MISSING_AUTH_TOKEN_MESSAGE = (
    """Sentry authentication token not found. Please specify your Sentry auth token."""
)


# Custom error class that is compatible with MCP error handling
class SentryMcpError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.error = message  # Add the error attribute that MCP expects


@dataclass
class SentryIssueData:
    title: str
    issue_id: str
    short_id: str = ""
    status: str = ""
    level: str = ""
    first_seen: str = ""
    last_seen: str = ""
    count: int = 0
    stacktrace: str = ""
    request_data: str = ""
    session_id: str = ""
    user_id: str = ""
    url: str = ""
    environment: str = ""
    project_name: str = ""
    request_id: str = ""
    response_body: str = ""

    def to_text(self) -> str:
        return f"""
Sentry Issue: {self.title}
Issue ID: {self.issue_id}
Short ID: {self.short_id}
Status: {self.status}
Level: {self.level}
Environment: {self.environment}
Project: {self.project_name}
First Seen: {self.first_seen}
Last Seen: {self.last_seen}
Event Count: {self.count}
Session ID: {self.session_id}
User ID: {self.user_id}
URL: {self.url}

** Failed Request Data **
Method: POST
Request ID: {self.request_id}
URL: {self.url}
Response Body: {self.response_body}

{self.stacktrace}
        """

    def to_prompt_result(self) -> types.GetPromptResult:
        return types.GetPromptResult(
            description=f"Sentry Issue: {self.title}",
            messages=[
                types.PromptMessage(
                    role="user", content=types.TextContent(type="text", text=self.to_text())
                )
            ],
        )

    def to_tool_result(self) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        return [types.TextContent(type="text", text=self.to_text())]


class SentryError(Exception):
    pass


def extract_issue_id(issue_id_or_url: str) -> str:
    """
    Extracts the Sentry issue ID from either a full URL or a standalone ID.

    This function validates the input and returns the numeric issue ID.
    It raises SentryError for invalid inputs, including empty strings,
    non-Sentry URLs, malformed paths, and non-numeric IDs.
    """
    if not issue_id_or_url:
        raise SentryError("Missing issue_id_or_url argument")

    if issue_id_or_url.startswith(("http://", "https://")):
        parsed_url = urlparse(issue_id_or_url)
        if not parsed_url.hostname or not parsed_url.hostname.endswith(".sentry.io"):
            raise SentryError("Invalid Sentry URL. Must be a URL ending with .sentry.io")

        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) < 2 or path_parts[0] != "issues":
            raise SentryError(
                "Invalid Sentry issue URL. Path must contain '/issues/{issue_id}'"
            )

        issue_id = path_parts[-1]
    else:
        issue_id = issue_id_or_url

    if not issue_id.isdigit():
        raise SentryError("Invalid Sentry issue ID. Must be a numeric value.")

    return issue_id


def create_stacktrace(latest_event: dict) -> str:
    """
    Creates a formatted stacktrace string from the latest Sentry event.

    This function extracts exception information and stacktrace details from the
    provided event dictionary, formatting them into a human-readable string.
    It handles multiple exceptions and includes file, line number, and function
    information for each frame in the stacktrace.

    Args:
        latest_event (dict): A dictionary containing the latest Sentry event data.

    Returns:
        str: A formatted string containing the stacktrace information,
             or "No stacktrace found" if no relevant data is present.
    """
    stacktraces = []
    for entry in latest_event.get("entries", []):
        if entry["type"] != "exception":
            continue

        exception_data = entry["data"]["values"]
        for exception in exception_data:
            exception_type = exception.get("type", "Unknown")
            exception_value = exception.get("value", "")
            stacktrace = exception.get("stacktrace")

            stacktrace_text = f"Exception: {exception_type}: {exception_value}\n\n"
            if stacktrace:
                stacktrace_text += "Stacktrace:\n"
                for frame in stacktrace.get("frames", []):
                    filename = frame.get("filename", "Unknown")
                    lineno = frame.get("lineNo", "?")
                    function = frame.get("function", "Unknown")

                    stacktrace_text += f"{filename}:{lineno} in {function}\n"

                    if "context" in frame:
                        context = frame["context"]
                        for ctx_line in context:
                            stacktrace_text += f"    {ctx_line[1]}\n"

                    stacktrace_text += "\n"

            stacktraces.append(stacktrace_text)

    return "\n".join(stacktraces) if stacktraces else "No stacktrace found"


def extract_request_data(event: dict) -> str:
    """
    Extracts and formats request data from a Sentry event.
    
    Args:
        event (dict): The Sentry event data
        
    Returns:
        str: Formatted request data or empty string if not available
    """
    if "request" not in event:
        return ""
    
    request = event["request"]
    method = request.get("method", "")
    request_id = request.get("headers", {}).get("request-id", "")
    url = request.get("url", "")
    
    # Extract response body if available
    response_body = ""
    if "data" in request and isinstance(request["data"], dict):
        response_body = request["data"].get("responseBody", "")
    
    # If we have no data, don't show the request data section
    if not (method or request_id or url or response_body):
        return ""
    
    return f"""** Failed Request Data **
Method: {method}
Request ID: {request_id}
URL: {url}
Response Body: {response_body}"""


async def handle_sentry_issue(
    http_client: httpx.AsyncClient, auth_token: str, issue_id_or_url: str
) -> Dict[str, Any]:
    """
    Fetches issue data from Sentry API.
    Returns the raw data for debugging.
    """
    try:
        if not issue_id_or_url:
            raise SentryError("Missing issue_id_or_url argument")
            
        issue_id = extract_issue_id(issue_id_or_url)

        response = await http_client.get(
            f"issues/{issue_id}/", headers={"Authorization": f"Bearer {auth_token}"}
        )
        if response.status_code == 401:
            raise SentryMcpError(
                "Error: Unauthorized. Please check your MCP_SENTRY_AUTH_TOKEN token."
            )
        response.raise_for_status()
        issue_data = response.json()

        # Get issue hashes
        hashes_response = await http_client.get(
            f"issues/{issue_id}/hashes/",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        hashes_response.raise_for_status()
        hashes = hashes_response.json()

        if not hashes:
            raise SentryMcpError("No Sentry events found for this issue")
            
        # Get the raw data for debugging
        raw_data = {
            "issue_data": issue_data,
            "hashes": hashes
        }
        
        # Now create a properly formatted SentryIssueData object
        latest_event = hashes[0]["latestEvent"]
        stacktrace = create_stacktrace(latest_event)
        
        # Extract data from raw_data
        project_name = issue_data.get("project", {}).get("name", "")
        short_id = issue_data.get("shortId", "")
        
        # Extract session ID, user ID, and URL from tags
        session_id = ""
        user_id = ""
        url = ""
        environment = ""
        
        # Extract from tags
        for tag in latest_event.get("tags", []):
            key = tag.get("key", "")
            if key == "sessionId":
                session_id = tag.get("value", "")
            elif key == "user":
                user_value = tag.get("value", "")
                # Parse user ID from format like "id:user-9V0giID-m9fj3IqgaUfN5meZ"
                if user_value.startswith("id:"):
                    user_id = user_value[3:]
            elif key == "url":
                url = tag.get("value", "")
            elif key == "environment":
                environment = tag.get("value", "")
        
        # If user ID not found in tags, look in user object
        if not user_id and "user" in latest_event:
            user_id = latest_event["user"].get("id", "")
        
        # If URL not found in tags, look in request
        if not url and "request" in latest_event:
            url = latest_event["request"].get("url", "")
            
        # Extract request data from contexts
        request_id = ""
        response_body = ""
        failed_request_data = latest_event.get("contexts", {}).get("** Failed Request Data **", {})
        if failed_request_data:
            request_id = failed_request_data.get("requestId", "")
            response_body = failed_request_data.get("responseBody", "")
        
        sentry_issue = SentryIssueData(
            title=issue_data.get("title", ""),
            issue_id=issue_id,
            short_id=short_id,
            status=issue_data.get("status", ""),
            level=issue_data.get("level", ""),
            first_seen=issue_data.get("firstSeen", ""),
            last_seen=issue_data.get("lastSeen", ""),
            count=int(issue_data.get("count", 0)),
            stacktrace=stacktrace,
            session_id=session_id,
            user_id=user_id,
            url=url,
            environment=environment,
            project_name=project_name,
            request_id=request_id,
            response_body=response_body
        )
        
        # Include both raw data and formatted data for debugging purposes
        return {
            "raw_data": raw_data,
            "formatted_data": sentry_issue
        }
        
    except SentryError as e:
        raise SentryMcpError(str(e))
    except httpx.HTTPStatusError as e:
        raise SentryMcpError(f"Error fetching Sentry issue: {str(e)}")
    except Exception as e:
        raise SentryMcpError(f"An error occurred: {str(e)}")


async def serve(auth_token: str) -> Server:
    server = Server("sentry")
    http_client = httpx.AsyncClient(base_url=SENTRY_API_BASE)

    @server.list_prompts()
    async def handle_list_prompts() -> list[types.Prompt]:
        return [
            types.Prompt(
                name="sentry-issue",
                description="Retrieve a Sentry issue by ID or URL",
                arguments=[
                    types.PromptArgument(
                        name="issue_id_or_url",
                        description="Sentry issue ID or URL",
                        required=True,
                    )
                ],
            )
        ]

    @server.get_prompt()
    async def handle_get_prompt(
        name: str, arguments: dict[str, str] | None
    ) -> types.GetPromptResult:
        try:
            if name != "sentry-issue":
                raise SentryMcpError(f"Unknown prompt: {name}")

            issue_id_or_url = (arguments or {}).get("issue_id_or_url", "")
            if not issue_id_or_url:
                raise SentryMcpError("Missing issue_id_or_url argument")
            
            result = await handle_sentry_issue(http_client, auth_token, issue_id_or_url)
            
            # Use the formatted data for display
            if "formatted_data" in result and isinstance(result["formatted_data"], SentryIssueData):
                return result["formatted_data"].to_prompt_result()
            
            # Fallback to raw JSON if something went wrong with formatting
            debug_text = json.dumps(result, indent=2)
            return types.GetPromptResult(
                description="Sentry Issue Debug Data",
                messages=[
                    types.PromptMessage(
                        role="user", 
                        content=types.TextContent(type="text", text=debug_text)
                    )
                ],
            )
        except Exception as e:
            if not hasattr(e, "error"):
                raise SentryMcpError(str(e))
            raise e

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="get_sentry_issue",
                description="""Retrieve and analyze a Sentry issue by ID or URL. Use this tool when you need to:
                - Investigate production errors and crashes
                - Access detailed stacktraces from Sentry
                - Analyze error patterns and frequencies
                - Get information about when issues first/last occurred
                - Review error counts and status""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "issue_id_or_url": {
                            "type": "string",
                            "description": "Sentry issue ID or URL to analyze"
                        }
                    },
                    "required": ["issue_id_or_url"]
                }
            )
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        try:
            if name != "get_sentry_issue":
                raise SentryMcpError(f"Unknown tool: {name}")

            if not arguments or "issue_id_or_url" not in arguments:
                raise SentryMcpError("Missing issue_id_or_url argument")

            result = await handle_sentry_issue(http_client, auth_token, arguments["issue_id_or_url"])
            
            # Use the formatted data for display
            if "formatted_data" in result and isinstance(result["formatted_data"], SentryIssueData):
                return result["formatted_data"].to_tool_result()
            
            # Fallback to raw JSON if something went wrong with formatting
            debug_text = json.dumps(result, indent=2)
            return [types.TextContent(type="text", text=debug_text)]
        except Exception as e:
            if not hasattr(e, "error"):
                raise SentryMcpError(str(e))
            raise e

    return server

@click.command()
@click.option(
    "--auth-token",
    envvar="SENTRY_TOKEN",
    required=True,
    help="Sentry authentication token",
)
def main(auth_token: str):
    async def _run():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            server = await serve(auth_token)
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="sentry",
                    server_version="0.4.1",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )

    asyncio.run(_run())
