# server.py
import sys
import os
import json
import httpx
from typing import Dict, List, Optional, Any, Union
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Notion MCP")

# Environment variables for Notion configuration
NOTION_BASE_URL = os.environ.get("NOTION_BASE_URL", "https://api.notion.com/v1")
NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
NOTION_VERSION = os.environ.get("NOTION_VERSION", "2022-06-28")

# Check if environment variables are set
if not NOTION_API_KEY:
    print("Warning: Notion environment variables not fully configured. Set NOTION_API_KEY.", file=sys.stderr)

# Helper function for API requests
async def make_notion_request(method: str, endpoint: str, data: Dict = None) -> Dict:
    """
    Make a request to the Notion API.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint (without base URL)
        data: Data to send (for POST/PUT)
    
    Returns:
        Response from Notion API as dictionary
    """
    url = f"{NOTION_BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
        "Accept": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        if method.upper() == "GET":
            response = await client.get(url, headers=headers)
        elif method.upper() == "POST":
            response = await client.post(url, headers=headers, json=data)
        elif method.upper() == "PUT":
            response = await client.put(url, headers=headers, json=data)
        elif method.upper() == "PATCH":
            response = await client.patch(url, headers=headers, json=data)
        elif method.upper() == "DELETE":
            response = await client.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        if response.status_code >= 400:
            return {
                "error": True,
                "status_code": response.status_code,
                "message": response.text
            }
            
        return response.json()

# === TOOLS ===

@mcp.tool()
async def search_notion(query: str, filter_type: Optional[str] = None) -> str:
    """
    Search Notion content.
    
    Args:
        query: The search query text
        filter_type: Optional filter for page or database (leave empty for all)
    """
    payload = {"query": query}
    
    if filter_type:
        if filter_type.lower() in ["page", "database"]:
            payload["filter"] = {"value": filter_type.lower(), "property": "object"}
    
    result = await make_notion_request("POST", "/search", payload)
    
    if "error" in result:
        return f"Error searching Notion: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_page(page_id: str) -> str:
    """
    Get details of a specific Notion page.
    
    Args:
        page_id: The Notion page ID (UUID)
    """
    # Clean the page ID if it contains dashes or full URL
    if "/" in page_id:
        page_id = page_id.split("/")[-1]
    page_id = page_id.replace("-", "")
    
    result = await make_notion_request("GET", f"/pages/{page_id}")
    
    if "error" in result:
        return f"Error retrieving page: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_block_children(block_id: str, page_size: int = 100) -> str:
    """
    Get children blocks of a block or page.
    
    Args:
        block_id: The Notion block or page ID
        page_size: Number of results to return (max 100)
    """
    # Clean the block ID if it contains dashes or full URL
    if "/" in block_id:
        block_id = block_id.split("/")[-1]
    block_id = block_id.replace("-", "")
    
    result = await make_notion_request("GET", f"/blocks/{block_id}/children?page_size={page_size}")
    
    if "error" in result:
        return f"Error retrieving blocks: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_database(database_id: str) -> str:
    """
    Get details of a specific Notion database.
    
    Args:
        database_id: The Notion database ID (UUID)
    """
    # Clean the database ID if it contains dashes or full URL
    if "/" in database_id:
        database_id = database_id.split("/")[-1]
    database_id = database_id.replace("-", "")
    
    result = await make_notion_request("GET", f"/databases/{database_id}")
    
    if "error" in result:
        return f"Error retrieving database: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def query_database(database_id: str, filter_json: Optional[str] = None, sorts_json: Optional[str] = None, page_size: int = 100) -> str:
    """
    Query a Notion database with optional filters and sorting.
    
    Args:
        database_id: The Notion database ID (UUID)
        filter_json: Optional JSON string with filter criteria
        sorts_json: Optional JSON string with sorting criteria
        page_size: Number of results to return (max 100)
    """
    # Clean the database ID if it contains dashes or full URL
    if "/" in database_id:
        database_id = database_id.split("/")[-1]
    database_id = database_id.replace("-", "")
    
    payload = {"page_size": page_size}
    
    if filter_json:
        try:
            payload["filter"] = json.loads(filter_json)
        except json.JSONDecodeError:
            return "Error: Invalid filter JSON format"
    
    if sorts_json:
        try:
            payload["sorts"] = json.loads(sorts_json)
        except json.JSONDecodeError:
            return "Error: Invalid sorts JSON format"
    
    result = await make_notion_request("POST", f"/databases/{database_id}/query", payload)
    
    if "error" in result:
        return f"Error querying database: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def create_page(parent_id: str, parent_type: str = "database_id", properties_json: Optional[str] = None, content_json: Optional[str] = None) -> str:
    """
    Create a new page in Notion.
    
    Args:
        parent_id: The parent database ID or page ID
        parent_type: Type of parent ('database_id' or 'page_id')
        properties_json: JSON string with page properties
        content_json: Optional JSON string with page content blocks
    """
    # Clean the parent ID if it contains dashes or full URL
    if "/" in parent_id:
        parent_id = parent_id.split("/")[-1]
    parent_id = parent_id.replace("-", "")
    
    if parent_type not in ["database_id", "page_id"]:
        return "Error: parent_type must be either 'database_id' or 'page_id'"
    
    try:
        properties = json.loads(properties_json) if properties_json else {}
    except json.JSONDecodeError:
        return "Error: Invalid properties JSON format"
    
    payload = {
        "parent": {parent_type: parent_id},
        "properties": properties
    }
    
    if content_json:
        try:
            content = json.loads(content_json)
            if isinstance(content, list):
                payload["children"] = content
            else:
                return "Error: content_json must be a JSON array of block objects"
        except json.JSONDecodeError:
            return "Error: Invalid content JSON format"
    
    result = await make_notion_request("POST", "/pages", payload)
    
    if "error" in result:
        return f"Error creating page: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def update_page(page_id: str, properties_json: str) -> str:
    """
    Update properties of an existing Notion page.
    
    Args:
        page_id: The ID of the page to update
        properties_json: JSON string with page properties to update
    """
    # Clean the page ID if it contains dashes or full URL
    if "/" in page_id:
        page_id = page_id.split("/")[-1]
    page_id = page_id.replace("-", "")
    
    try:
        properties = json.loads(properties_json)
    except json.JSONDecodeError:
        return "Error: Invalid properties JSON format"
    
    payload = {"properties": properties}
    
    result = await make_notion_request("PATCH", f"/pages/{page_id}", payload)
    
    if "error" in result:
        return f"Error updating page: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def append_blocks(block_id: str, blocks_json: str) -> str:
    """
    Append new blocks to an existing block or page.
    
    Args:
        block_id: The ID of the block or page to append to
        blocks_json: JSON array of block objects to append
    """
    # Clean the block ID if it contains dashes or full URL
    if "/" in block_id:
        block_id = block_id.split("/")[-1]
    block_id = block_id.replace("-", "")
    
    try:
        blocks = json.loads(blocks_json)
        if not isinstance(blocks, list):
            return "Error: blocks_json must be a JSON array of block objects"
    except json.JSONDecodeError:
        return "Error: Invalid blocks JSON format"
    
    payload = {"children": blocks}
    
    result = await make_notion_request("PATCH", f"/blocks/{block_id}/children", payload)
    
    if "error" in result:
        return f"Error appending blocks: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

# === RESOURCES ===

@mcp.resource("notion://search")
async def search_resource() -> str:
    """Search all Notion content."""
    result = await make_notion_request("POST", "/search", {})
    
    if "error" in result:
        return f"Error retrieving Notion search results: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.resource("notion://databases")
async def get_databases() -> str:
    """Get a list of databases the user has access to."""
    # Notion doesn't have a direct endpoint to list all databases, so we use search with a filter
    result = await make_notion_request("POST", "/search", {"filter": {"value": "database", "property": "object"}})
    
    if "error" in result:
        return f"Error retrieving databases: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.resource("notion://users")
async def get_users() -> str:
    """Get a list of all users in the workspace."""
    result = await make_notion_request("GET", "/users")
    
    if "error" in result:
        return f"Error retrieving users: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

# === PROMPTS ===

@mcp.prompt("create_database_entry")
def create_database_entry_prompt(database_id: str = None, title: str = None):
    """
    A prompt template for creating a new entry in a Notion database.
    
    Args:
        database_id: ID of the database
        title: Title of the new entry
    """
    if all([database_id, title]):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please help me create a new entry in my Notion database with ID {database_id}. The entry should be titled '{title}'. What other information should I include?"
                    }
                }
            ]
        }
    else:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": "I need to create a new entry in my Notion database. Please help me with the required details."
                    }
                }
            ]
        }

@mcp.prompt("search_and_summarize")
def search_and_summarize_prompt(query: str = None):
    """
    A prompt template for searching Notion and summarizing results.
    
    Args:
        query: Search query
    """
    if query:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please search my Notion workspace for '{query}' and summarize the key information found in the results."
                    }
                }
            ]
        }
    else:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": "I'd like to search my Notion workspace and get a summary of the results. What topic should I search for?"
                    }
                }
            ]
        }

@mcp.prompt("database_query_builder")
def database_query_builder_prompt(database_id: str = None):
    """
    A prompt template for building Notion database queries.
    
    Args:
        database_id: ID of the database to query
    """
    if database_id:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"I want to query my Notion database with ID {database_id}. Please help me build a query with filters and sorting options."
                    }
                }
            ]
        }
    else:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": "I want to query one of my Notion databases. Please help me build a query with filters and sorting options."
                    }
                }
            ]
        }

if __name__ == "__main__":
    print("Starting Notion MCP server...", file=sys.stderr)
    mcp.run()
