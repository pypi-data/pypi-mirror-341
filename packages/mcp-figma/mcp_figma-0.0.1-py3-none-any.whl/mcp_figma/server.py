# server.py
import sys
import os
import json
from typing import Dict, List, Optional, Any, Union
import httpx
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Figma MCP")

# Environment variables for Figma configuration
FIGMA_BASE_URL = os.environ.get("FIGMA_BASE_URL", "https://api.figma.com/v1")
FIGMA_ACCESS_TOKEN = os.environ.get("FIGMA_ACCESS_TOKEN")

# Check if environment variables are set
if not FIGMA_ACCESS_TOKEN:
    print("Warning: Figma environment variables not fully configured. Set FIGMA_ACCESS_TOKEN.", file=sys.stderr)

# Helper function for API requests
async def make_figma_request(method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict:
    """
    Make a request to the Figma API.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint (without base URL)
        data: Data to send (for POST/PUT)
        params: Query parameters (for GET)
    
    Returns:
        Response from Figma API as dictionary
    """
    url = f"{FIGMA_BASE_URL}{endpoint}"
    headers = {
        "X-Figma-Token": FIGMA_ACCESS_TOKEN,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, params=params, timeout=30.0)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=data, timeout=30.0)
            elif method.upper() == "PUT":
                response = await client.put(url, headers=headers, json=data, timeout=30.0)
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers, timeout=30.0)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_message = f"HTTP Error: {e.response.status_code}"
            try:
                error_data = e.response.json()
                error_message += f" - {error_data.get('message', 'Unknown error')}"
            except:
                error_message += f" - {e.response.text}"
            return {"error": True, "message": error_message}
        except httpx.RequestError as e:
            return {"error": True, "message": f"Request Error: {str(e)}"}
        except Exception as e:
            return {"error": True, "message": f"Error: {str(e)}"}

# Format large JSON response for readability
def format_response(response: Dict) -> str:
    """Format API response for readability."""
    # Check if response is an error
    if isinstance(response, dict) and response.get("error"):
        return f"Error: {response.get('message', 'Unknown error')}"
    
    # Format successful response
    return json.dumps(response, indent=2)

# === TOOLS ===

@mcp.tool()
async def get_file(file_key: str) -> str:
    """
    Get details of a specific Figma file.
    
    Args:
        file_key: The Figma file key (found in the URL after figma.com/file/)
    """
    result = await make_figma_request("GET", f"/files/{file_key}")
    return format_response(result)

@mcp.tool()
async def get_file_nodes(file_key: str, node_ids: str) -> str:
    """
    Get specific nodes from a Figma file.
    
    Args:
        file_key: The Figma file key
        node_ids: Comma-separated list of node IDs
    """
    ids_list = [id.strip() for id in node_ids.split(",")]
    params = {"ids": ",".join(ids_list)}
    result = await make_figma_request("GET", f"/files/{file_key}/nodes", params=params)
    return format_response(result)

@mcp.tool()
async def get_comments(file_key: str) -> str:
    """
    Get comments from a Figma file.
    
    Args:
        file_key: The Figma file key
    """
    result = await make_figma_request("GET", f"/files/{file_key}/comments")
    return format_response(result)

@mcp.tool()
async def create_comment(file_key: str, message: str, position_x: float, position_y: float, node_id: Optional[str] = None) -> str:
    """
    Create a comment on a Figma file.
    
    Args:
        file_key: The Figma file key
        message: Comment text
        position_x: X position in the file
        position_y: Y position in the file
        node_id: Optional node ID to attach the comment to
    """
    comment_data = {
        "message": message,
        "client_meta": {
            "x": position_x,
            "y": position_y
        }
    }
    
    if node_id:
        comment_data["node_id"] = node_id
    
    result = await make_figma_request("POST", f"/files/{file_key}/comments", data=comment_data)
    return format_response(result)

@mcp.tool()
async def get_file_versions(file_key: str) -> str:
    """
    Get version history of a Figma file.
    
    Args:
        file_key: The Figma file key
    """
    result = await make_figma_request("GET", f"/files/{file_key}/versions")
    return format_response(result)

@mcp.tool()
async def get_team_projects(team_id: str) -> str:
    """
    Get projects for a Figma team.
    
    Args:
        team_id: The Figma team ID
    """
    result = await make_figma_request("GET", f"/teams/{team_id}/projects")
    return format_response(result)

@mcp.tool()
async def get_project_files(project_id: str) -> str:
    """
    Get files in a Figma project.
    
    Args:
        project_id: The Figma project ID
    """
    result = await make_figma_request("GET", f"/projects/{project_id}/files")
    return format_response(result)

@mcp.tool()
async def export_image(file_key: str, node_ids: str, format: str = "png", scale: float = 1.0) -> str:
    """
    Export parts of a Figma document as images.
    
    Args:
        file_key: The Figma file key
        node_ids: Comma-separated list of node IDs to export
        format: Image format (png, jpg, svg, pdf)
        scale: Image scale (1-4)
    """
    ids_list = [id.strip() for id in node_ids.split(",")]
    params = {
        "ids": ",".join(ids_list),
        "format": format,
        "scale": scale
    }
    result = await make_figma_request("GET", f"/images/{file_key}", params=params)
    return format_response(result)

@mcp.tool()
async def get_component_sets(team_id: str) -> str:
    """
    Get component sets for a team.
    
    Args:
        team_id: The Figma team ID
    """
    result = await make_figma_request("GET", f"/teams/{team_id}/component_sets")
    return format_response(result)

@mcp.tool()
async def get_styles(team_id: str) -> str:
    """
    Get styles for a team.
    
    Args:
        team_id: The Figma team ID
    """
    result = await make_figma_request("GET", f"/teams/{team_id}/styles")
    return format_response(result)

# === RESOURCES ===

@mcp.resource("figma://me")
async def get_me() -> str:
    """Get information about the current user."""
    result = await make_figma_request("GET", "/me")
    return format_response(result)

@mcp.resource("figma://files")
async def get_files() -> str:
    """Get a list of recently accessed Figma files."""
    # Figma doesn't have a direct endpoint for listing all files
    # This is a placeholder - in a real implementation, you might need to
    # use the /projects/{project_id}/files endpoint for each project
    return json.dumps({
        "message": "To list files, please use the get_project_files tool with a specific project ID."
    }, indent=2)

@mcp.resource("figma://teams")
async def get_teams() -> str:
    """Get a list of Figma teams you belong to."""
    result = await make_figma_request("GET", "/teams")
    return format_response(result)

# === PROMPTS ===

@mcp.prompt("create_comment_prompt")
def create_comment_prompt(file_key: str = None, message: str = None, position_x: float = None, position_y: float = None):
    """
    A prompt template for creating a new comment in Figma.
    
    Args:
        file_key: The Figma file key
        message: Comment text
        position_x: X position in the file
        position_y: Y position in the file
    """
    if all([file_key, message, position_x, position_y]):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please help me create a new comment in Figma with these details:\n\nFile Key: {file_key}\nMessage: {message}\nPosition: ({position_x}, {position_y})"
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
                        "text": "I need to create a new comment in a Figma file. Please help me with the required details."
                    }
                }
            ]
        }

@mcp.prompt("analyze_design_prompt")
def analyze_design_prompt(file_key: str = None):
    """
    A prompt template for analyzing a Figma design file.
    
    Args:
        file_key: The Figma file key to analyze
    """
    if file_key:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please help me analyze the Figma design in file {file_key}. I'd like to understand the design system, component structure, and overall organization."
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
                        "text": "I need to analyze a Figma design. Please help me extract useful insights from it."
                    }
                }
            ]
        }

@mcp.prompt("export_assets_prompt")
def export_assets_prompt(file_key: str = None, node_ids: str = None):
    """
    A prompt template for exporting assets from a Figma design.
    
    Args:
        file_key: The Figma file key
        node_ids: Comma-separated list of node IDs to export
    """
    if all([file_key, node_ids]):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please help me export these assets from Figma:\n\nFile Key: {file_key}\nNode IDs: {node_ids}\n\nI need them in various formats for my project."
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
                        "text": "I need to export some assets from a Figma file. Please help me with the process."
                    }
                }
            ]
        }

if __name__ == "__main__":
    print("Starting Figma MCP server...", file=sys.stderr)
    mcp.run()