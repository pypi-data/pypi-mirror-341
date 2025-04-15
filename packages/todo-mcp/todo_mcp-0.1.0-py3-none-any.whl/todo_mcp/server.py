import asyncio

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio
import os
import json
import requests

# Supabase API credentials
base_url = "http://localhost:8000/rest/v1/todos"
api_key = os.environ.get("SUPABASE_API_KEY")
auth_token = os.environ.get("SUPABASE_AUTH_TOKEN")

# Store notes as a simple key-value dict to demonstrate state management
notes: dict[str, str] = {}

server = Server(
    "todo-mcp",
)

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """
    List available note resources.
    Each note is exposed as a resource with a custom note:// URI scheme.
    """
    return [
        types.Resource(
            uri=AnyUrl(f"note://internal/{name}"),
            name=f"Note: {name}",
            description=f"A simple note named {name}",
            mimeType="text/plain",
        )
        for name in notes
    ]

@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """
    Read a specific note's content by its URI.
    The note name is extracted from the URI host component.
    """
    if uri.scheme != "note":
        raise ValueError(f"Unsupported URI scheme: {uri.scheme}")

    name = uri.path
    if name is not None:
        name = name.lstrip("/")
        return notes[name]
    raise ValueError(f"Note not found: {name}")

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """
    List available prompts.
    Each prompt can have optional arguments to customize its behavior.
    """
    return [
        types.Prompt(
            name="summarize-notes",
            description="Creates a summary of all notes",
            arguments=[
                types.PromptArgument(
                    name="style",
                    description="Style of the summary (brief/detailed)",
                    required=False,
                )
            ],
        )
    ]

@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """
    Generate a prompt by combining arguments with server state.
    The prompt includes all current notes and can be customized via arguments.
    """
    if name != "summarize-notes":
        raise ValueError(f"Unknown prompt: {name}")

    style = (arguments or {}).get("style", "brief")
    detail_prompt = " Give extensive details." if style == "detailed" else ""

    return types.GetPromptResult(
        description="Summarize the current notes",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"Here are the current notes to summarize:{detail_prompt}\n\n"
                    + "\n".join(
                        f"- {name}: {content}"
                        for name, content in notes.items()
                    ),
                ),
            )
        ],
    )

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="add-note",
            description="Add a new note",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["name", "content"],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    """
    if name != "add-note":
        raise ValueError(f"Unknown tool: {name}")

    if not arguments:
        raise ValueError("Missing arguments")

    note_name = arguments.get("name")
    content = arguments.get("content")

    if not note_name or not content:
        raise ValueError("Missing name or content")

    # Update server state
    notes[note_name] = content

    # Notify clients that resources have changed
    await server.request_context.session.send_resource_list_changed()

    return [
        types.TextContent(
            type="text",
            text=f"Added note '{note_name}' with content: {content}",
        )
    ]

async def get_todos(arguments):
    select = arguments.get("select", "*")
    filter_param = arguments.get("filter")
    range_start = arguments.get("range_start")
    range_end = arguments.get("range_end")

    url = f"{base_url}?select={select}"
    if filter_param:
        url += f"&{filter_param}"

    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }

    if range_start is not None and range_end is not None:
        headers["Range"] = f"{range_start}-{range_end}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return {"content": [{"type": "text", "text": json.dumps(response.json(), indent=2)}]}
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")


async def insert_todo(arguments):
    task = arguments["task"]
    user_id = arguments["user_id"]
    is_complete = arguments.get("is_complete", False)

    url = base_url

    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }

    data = {"task": task, "user_id": user_id, "is_complete": is_complete}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return {"content": [{"type": "text", "text": "Todo item inserted successfully"}]}
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="add-note",
            description="Add a new note",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["name", "content"],
            },
        ),
        types.Tool(
            name="get_todos",
            description="Get todos from the API",
            inputSchema={
                "type": "object",
                "properties": {
                    "select": {
                        "type": "string",
                        "description": "Columns to select (e.g., id, task, is_complete)",
                    },
                    "filter": {
                        "type": "string",
                        "description": "Filter conditions (e.g., task=eq.MyTask)",
                    },
                    "range_start": {
                        "type": "integer",
                        "description": "Pagination start range",
                    },
                    "range_end": {
                        "type": "integer",
                        "description": "Pagination end range",
                    },
                },
            },
        ),
        types.Tool(
            name="insert_todo",
            description="Insert a new todo item",
            inputSchema={
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The task to add",
                    },
                    "user_id": {
                        "type": "string",
                        "description": "The user ID",
                    },
                    "is_complete": {
                        "type": "boolean",
                        "description": "Is the task complete?",
                    },
                },
                "required": ["task", "user_id"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    """
    if name == "add-note":
        if not arguments:
            raise ValueError("Missing arguments")

        note_name = arguments.get("name")
        content = arguments.get("content")

        if not note_name or not content:
            raise ValueError("Missing name or content")

        # Update server state
        notes[note_name] = content

        # Notify clients that resources have changed
        await server.request_context.session.send_resource_list_changed()

        return [
            types.TextContent(
                type="text",
                text=f"Added note '{note_name}' with content: {content}",
            )
        ]
    elif name == "get_todos":
        return await get_todos(arguments)
    elif name == "insert_todo":
        return await insert_todo(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="todo-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
