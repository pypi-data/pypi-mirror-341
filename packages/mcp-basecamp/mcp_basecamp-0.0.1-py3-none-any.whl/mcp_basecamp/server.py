# server.py
import sys
import os
import json
import httpx
from typing import Dict, List, Optional, Any, Union
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Basecamp MCP")

# Environment variables for Basecamp configuration
BASECAMP_BASE_URL = os.environ.get("BASECAMP_BASE_URL")
BASECAMP_API_KEY = os.environ.get("BASECAMP_API_KEY")
BASECAMP_ACCOUNT_ID = os.environ.get("BASECAMP_ACCOUNT_ID")
BASECAMP_USER_AGENT = os.environ.get("BASECAMP_USER_AGENT", "MCP Basecamp Server (your-email@example.com)")

# Check if environment variables are set
if not all([BASECAMP_BASE_URL, BASECAMP_API_KEY, BASECAMP_ACCOUNT_ID]):
    print("Warning: Basecamp environment variables not fully configured. Set BASECAMP_BASE_URL, BASECAMP_API_KEY, and BASECAMP_ACCOUNT_ID.", file=sys.stderr)

# Helper function for API requests
async def make_basecamp_request(method: str, endpoint: str, data: Dict = None) -> Dict:
    """
    Make a request to the Basecamp API.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint (without base URL)
        data: Data to send (for POST/PUT)
    
    Returns:
        Response from Basecamp API as dictionary
    """
    url = f"{BASECAMP_BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {BASECAMP_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": BASECAMP_USER_AGENT
    }
    
    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, timeout=30.0)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=data, timeout=30.0)
            elif method.upper() == "PUT":
                response = await client.put(url, headers=headers, json=data, timeout=30.0)
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers, timeout=30.0)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            
            if response.status_code == 204:  # No content
                return {"success": True}
                
            return response.json()
        except httpx.HTTPStatusError as e:
            error_message = f"HTTP Error: {e.response.status_code}"
            try:
                error_json = e.response.json()
                if isinstance(error_json, dict):
                    error_message = error_json.get("error", error_message)
            except:
                pass
            
            return {
                "error": True,
                "status_code": e.response.status_code,
                "message": error_message
            }
        except Exception as e:
            return {
                "error": True,
                "message": str(e)
            }

# === TOOLS ===

@mcp.tool()
async def get_projects() -> str:
    """
    Get a list of all active projects in Basecamp.
    """
    result = await make_basecamp_request("GET", f"/api/v1/{BASECAMP_ACCOUNT_ID}/projects.json")
    
    if "error" in result:
        return f"Error retrieving projects: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_project(project_id: int) -> str:
    """
    Get details of a specific Basecamp project.
    
    Args:
        project_id: The Basecamp project ID
    """
    result = await make_basecamp_request("GET", f"/api/v1/{BASECAMP_ACCOUNT_ID}/projects/{project_id}.json")
    
    if "error" in result:
        return f"Error retrieving project: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def create_project(name: str, description: str = "") -> str:
    """
    Create a new project in Basecamp.
    
    Args:
        name: The name of the project
        description: Optional description for the project
    """
    data = {
        "name": name,
        "description": description
    }
    
    result = await make_basecamp_request("POST", f"/api/v1/{BASECAMP_ACCOUNT_ID}/projects.json", data)
    
    if "error" in result:
        return f"Error creating project: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_todos(project_id: int) -> str:
    """
    Get all to-do lists for a project.
    
    Args:
        project_id: The Basecamp project ID
    """
    result = await make_basecamp_request("GET", f"/api/v1/{BASECAMP_ACCOUNT_ID}/projects/{project_id}/todolists.json")
    
    if "error" in result:
        return f"Error retrieving to-do lists: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_todo_list(project_id: int, todolist_id: int) -> str:
    """
    Get details of a specific to-do list.
    
    Args:
        project_id: The Basecamp project ID
        todolist_id: The to-do list ID
    """
    result = await make_basecamp_request("GET", f"/api/v1/{BASECAMP_ACCOUNT_ID}/projects/{project_id}/todolists/{todolist_id}.json")
    
    if "error" in result:
        return f"Error retrieving to-do list: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def create_todo_list(project_id: int, name: str, description: str = "") -> str:
    """
    Create a new to-do list in a project.
    
    Args:
        project_id: The Basecamp project ID
        name: The name of the to-do list
        description: Optional description for the to-do list
    """
    data = {
        "name": name,
        "description": description
    }
    
    result = await make_basecamp_request("POST", f"/api/v1/{BASECAMP_ACCOUNT_ID}/projects/{project_id}/todolists.json", data)
    
    if "error" in result:
        return f"Error creating to-do list: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def create_todo_item(project_id: int, todolist_id: int, content: str, assignee_ids: str = None, due_on: str = None) -> str:
    """
    Create a new to-do item in a to-do list.
    
    Args:
        project_id: The Basecamp project ID
        todolist_id: The to-do list ID
        content: The content of the to-do item
        assignee_ids: Optional comma-separated list of assignee IDs
        due_on: Optional due date (YYYY-MM-DD format)
    """
    data = {
        "content": content
    }
    
    if assignee_ids:
        data["assignee_ids"] = [int(id.strip()) for id in assignee_ids.split(",")]
    
    if due_on:
        data["due_on"] = due_on
    
    result = await make_basecamp_request("POST", f"/api/v1/{BASECAMP_ACCOUNT_ID}/projects/{project_id}/todolists/{todolist_id}/todos.json", data)
    
    if "error" in result:
        return f"Error creating to-do item: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_messages(project_id: int) -> str:
    """
    Get all messages for a project.
    
    Args:
        project_id: The Basecamp project ID
    """
    result = await make_basecamp_request("GET", f"/api/v1/{BASECAMP_ACCOUNT_ID}/projects/{project_id}/messages.json")
    
    if "error" in result:
        return f"Error retrieving messages: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def create_message(project_id: int, subject: str, content: str) -> str:
    """
    Create a new message in a project.
    
    Args:
        project_id: The Basecamp project ID
        subject: The subject of the message
        content: The content of the message
    """
    data = {
        "subject": subject,
        "content": content
    }
    
    result = await make_basecamp_request("POST", f"/api/v1/{BASECAMP_ACCOUNT_ID}/projects/{project_id}/messages.json", data)
    
    if "error" in result:
        return f"Error creating message: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_people() -> str:
    """
    Get a list of all people in the Basecamp account.
    """
    result = await make_basecamp_request("GET", f"/api/v1/{BASECAMP_ACCOUNT_ID}/people.json")
    
    if "error" in result:
        return f"Error retrieving people: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_person(person_id: int) -> str:
    """
    Get details of a specific person.
    
    Args:
        person_id: The Basecamp person ID
    """
    result = await make_basecamp_request("GET", f"/api/v1/{BASECAMP_ACCOUNT_ID}/people/{person_id}.json")
    
    if "error" in result:
        return f"Error retrieving person: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_schedule(project_id: int) -> str:
    """
    Get the schedule for a project.
    
    Args:
        project_id: The Basecamp project ID
    """
    result = await make_basecamp_request("GET", f"/api/v1/{BASECAMP_ACCOUNT_ID}/projects/{project_id}/calendar_events.json")
    
    if "error" in result:
        return f"Error retrieving schedule: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def create_schedule_event(project_id: int, summary: str, description: str, starts_at: str, ends_at: str) -> str:
    """
    Create a new schedule event in a project.
    
    Args:
        project_id: The Basecamp project ID
        summary: The summary of the event
        description: The description of the event
        starts_at: Start date and time (ISO 8601 format)
        ends_at: End date and time (ISO 8601 format)
    """
    data = {
        "summary": summary,
        "description": description,
        "starts_at": starts_at,
        "ends_at": ends_at
    }
    
    result = await make_basecamp_request("POST", f"/api/v1/{BASECAMP_ACCOUNT_ID}/projects/{project_id}/calendar_events.json", data)
    
    if "error" in result:
        return f"Error creating schedule event: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

# === RESOURCES ===

@mcp.resource("basecamp://projects")
async def list_projects_resource() -> str:
    """Get a list of all Basecamp projects."""
    result = await make_basecamp_request("GET", f"/api/v1/{BASECAMP_ACCOUNT_ID}/projects.json")
    
    if "error" in result:
        return f"Error retrieving projects: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.resource("basecamp://project/{project_id}")
async def project_resource(project_id: str) -> str:
    """
    Get details of a specific Basecamp project.
    
    Args:
        project_id: The Basecamp project ID
    """
    result = await make_basecamp_request("GET", f"/api/v1/{BASECAMP_ACCOUNT_ID}/projects/{project_id}.json")
    
    if "error" in result:
        return f"Error retrieving project: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.resource("basecamp://people")
async def list_people_resource() -> str:
    """Get a list of all people in the Basecamp account."""
    result = await make_basecamp_request("GET", f"/api/v1/{BASECAMP_ACCOUNT_ID}/people.json")
    
    if "error" in result:
        return f"Error retrieving people: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.resource("basecamp://project/{project_id}/todolist/{todolist_id}")
async def todolist_resource(project_id: str, todolist_id: str) -> str:
    """
    Get a specific to-do list with its items.
    
    Args:
        project_id: The Basecamp project ID
        todolist_id: The to-do list ID
    """
    result = await make_basecamp_request("GET", f"/api/v1/{BASECAMP_ACCOUNT_ID}/projects/{project_id}/todolists/{todolist_id}.json")
    
    if "error" in result:
        return f"Error retrieving to-do list: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.resource("basecamp://project/{project_id}/schedule")
async def schedule_resource(project_id: str) -> str:
    """
    Get the schedule for a project.
    
    Args:
        project_id: The Basecamp project ID
    """
    result = await make_basecamp_request("GET", f"/api/v1/{BASECAMP_ACCOUNT_ID}/projects/{project_id}/calendar_events.json")
    
    if "error" in result:
        return f"Error retrieving schedule: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

# === PROMPTS ===

@mcp.prompt("create_project")
def create_project_prompt(name: str = None, description: str = None):
    """
    A prompt template for creating a new project in Basecamp.
    
    Args:
        name: Name of the project
        description: Description of the project
    """
    if name:
        project_details = f"Name: {name}\n"
        if description:
            project_details += f"Description: {description}"
        else:
            project_details += "Please help me come up with a description for this project."
            
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"I need to create a new project in Basecamp with these details:\n\n{project_details}\n\nPlease help me finalize this and suggest any additional details I should consider."
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
                        "text": "I need to create a new project in Basecamp. Can you help me think through what information I need to provide and how to structure it effectively?"
                    }
                }
            ]
        }

@mcp.prompt("weekly_status")
def weekly_status_prompt(project_id: str = None, team: str = None):
    """
    A prompt template for creating a weekly status update.
    
    Args:
        project_id: Optional project ID to focus on
        team: Optional team name to mention
    """
    context = ""
    if project_id:
        context += f"For Project ID: {project_id}\n"
    if team:
        context += f"For Team: {team}\n"
    
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"{context}Please help me draft a weekly status update for Basecamp that includes:\n\n1. Accomplishments from last week\n2. Plans for the coming week\n3. Any blockers or issues\n4. Questions for the team"
                }
            }
        ]
    }

@mcp.prompt("todo_list")
def todo_list_prompt(project_name: str = None, deadline: str = None):
    """
    A prompt template for creating a to-do list.
    
    Args:
        project_name: Optional project name for context
        deadline: Optional deadline for the to-dos
    """
    context = ""
    if project_name:
        context += f"For Project: {project_name}\n"
    if deadline:
        context += f"Deadline: {deadline}\n"
    
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"{context}Please help me create a comprehensive to-do list that I can add to Basecamp. I want to make sure I'm capturing all the key tasks and organizing them effectively."
                }
            }
        ]
    }

if __name__ == "__main__":
    print("Starting Basecamp MCP server...", file=sys.stderr)
    mcp.run()
