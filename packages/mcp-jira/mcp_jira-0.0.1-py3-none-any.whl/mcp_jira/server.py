# server.py
import sys
import os
import json
import httpx
from typing import Dict, List, Optional, Any, Union
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Jira MCP")

# Environment variables for Jira configuration
JIRA_BASE_URL = os.environ.get("JIRA_BASE_URL")
JIRA_USERNAME = os.environ.get("JIRA_USERNAME")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")

# Check if environment variables are set
if not all([JIRA_BASE_URL, JIRA_USERNAME, JIRA_API_TOKEN]):
    print("Warning: Jira environment variables not fully configured. Set JIRA_BASE_URL, JIRA_USERNAME, and JIRA_API_TOKEN.", file=sys.stderr)

# Jira headers for authentication
def get_headers():
    """Get headers with authentication for Jira API requests."""
    import base64
    auth_str = f"{JIRA_USERNAME}:{JIRA_API_TOKEN}"
    auth_bytes = auth_str.encode("ascii")
    auth_b64 = base64.b64encode(auth_bytes).decode("ascii")
    return {
        "Authorization": f"Basic {auth_b64}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

# Helper function for API requests
async def make_jira_request(method: str, endpoint: str, data: Dict = None) -> Dict:
    """
    Make a request to the Jira API.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint (without base URL)
        data: Data to send (for POST/PUT)
    
    Returns:
        Response from Jira API as dictionary
    """
    url = f"{JIRA_BASE_URL}{endpoint}"
    headers = get_headers()
    
    async with httpx.AsyncClient() as client:
        if method.upper() == "GET":
            response = await client.get(url, headers=headers)
        elif method.upper() == "POST":
            response = await client.post(url, headers=headers, json=data)
        elif method.upper() == "PUT":
            response = await client.put(url, headers=headers, json=data)
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
async def get_issue(issue_key: str) -> str:
    """
    Get details of a specific Jira issue.
    
    Args:
        issue_key: The Jira issue key (e.g., PROJ-123)
    """
    result = await make_jira_request("GET", f"/rest/api/2/issue/{issue_key}")
    
    if "error" in result:
        return f"Error retrieving issue: {result.get('message', 'Unknown error')}"
    
    # Format the issue details in a readable way
    fields = result.get("fields", {})
    formatted = [
        f"Issue: {result.get('key', 'Unknown')}",
        f"Summary: {fields.get('summary', 'No summary')}",
        f"Status: {fields.get('status', {}).get('name', 'Unknown')}",
        f"Type: {fields.get('issuetype', {}).get('name', 'Unknown')}",
        f"Priority: {fields.get('priority', {}).get('name', 'Unknown')}",
        f"Assignee: {fields.get('assignee', {}).get('displayName', 'Unassigned')}",
        f"Reporter: {fields.get('reporter', {}).get('displayName', 'Unknown')}",
        f"Created: {fields.get('created', 'Unknown')}",
        f"Updated: {fields.get('updated', 'Unknown')}",
        "",
        "Description:",
        fields.get('description', 'No description')
    ]
    
    return "\n".join(formatted)

@mcp.tool()
async def search_issues(jql: str, max_results: int = 10) -> str:
    """
    Search for Jira issues using JQL (Jira Query Language).
    
    Args:
        jql: JQL query string (e.g., "project = PROJ AND status = Open")
        max_results: Maximum number of results to return (default: 10)
    """
    data = {
        "jql": jql,
        "maxResults": max_results,
        "fields": ["key", "summary", "status", "issuetype", "priority", "assignee"]
    }
    
    result = await make_jira_request("POST", "/rest/api/2/search", data)
    
    if "error" in result:
        return f"Error searching issues: {result.get('message', 'Unknown error')}"
    
    issues = result.get("issues", [])
    if not issues:
        return "No issues found matching the query."
    
    formatted = [f"Found {len(issues)} issues:"]
    
    for issue in issues:
        fields = issue.get("fields", {})
        status = fields.get("status", {}).get("name", "Unknown")
        assignee = fields.get("assignee", {}).get("displayName", "Unassigned")
        
        formatted.append(
            f"{issue.get('key')}: {fields.get('summary', 'No summary')} "
            f"[{status}] - Assigned to: {assignee}"
        )
    
    return "\n".join(formatted)

@mcp.tool()
async def create_issue(
    project_key: str, 
    summary: str, 
    description: str, 
    issue_type: str = "Task", 
    priority: str = "Medium"
) -> str:
    """
    Create a new Jira issue.
    
    Args:
        project_key: The project key (e.g., PROJ)
        summary: Issue summary/title
        description: Detailed description
        issue_type: Type of issue (default: Task)
        priority: Priority level (default: Medium)
    """
    data = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type},
            "priority": {"name": priority}
        }
    }
    
    result = await make_jira_request("POST", "/rest/api/2/issue", data)
    
    if "error" in result:
        return f"Error creating issue: {result.get('message', 'Unknown error')}"
    
    return f"Issue created successfully: {result.get('key', 'Unknown')}"

@mcp.tool()
async def update_issue(
    issue_key: str, 
    summary: Optional[str] = None, 
    description: Optional[str] = None,
    priority: Optional[str] = None,
    assignee: Optional[str] = None
) -> str:
    """
    Update an existing Jira issue.
    
    Args:
        issue_key: The Jira issue key (e.g., PROJ-123)
        summary: New summary (optional)
        description: New description (optional)
        priority: New priority (optional)
        assignee: Username or email of assignee (optional)
    """
    fields = {}
    
    if summary:
        fields["summary"] = summary
    
    if description:
        fields["description"] = description
    
    if priority:
        fields["priority"] = {"name": priority}
    
    if assignee:
        fields["assignee"] = {"name": assignee}
    
    if not fields:
        return "No fields provided for update."
    
    data = {"fields": fields}
    result = await make_jira_request("PUT", f"/rest/api/2/issue/{issue_key}", data)
    
    if "error" in result:
        return f"Error updating issue: {result.get('message', 'Unknown error')}"
    
    return f"Issue {issue_key} updated successfully."

@mcp.tool()
async def add_comment(issue_key: str, comment: str) -> str:
    """
    Add a comment to a Jira issue.
    
    Args:
        issue_key: The Jira issue key (e.g., PROJ-123)
        comment: Comment text
    """
    data = {"body": comment}
    result = await make_jira_request("POST", f"/rest/api/2/issue/{issue_key}/comment", data)
    
    if "error" in result:
        return f"Error adding comment: {result.get('message', 'Unknown error')}"
    
    return f"Comment added successfully to issue {issue_key}."

@mcp.tool()
async def transition_issue(issue_key: str, transition_name: str) -> str:
    """
    Change the status of a Jira issue.
    
    Args:
        issue_key: The Jira issue key (e.g., PROJ-123)
        transition_name: Name of the transition (e.g., "In Progress", "Done")
    """
    # First, get available transitions
    transitions_result = await make_jira_request("GET", f"/rest/api/2/issue/{issue_key}/transitions")
    
    if "error" in transitions_result:
        return f"Error getting transitions: {transitions_result.get('message', 'Unknown error')}"
    
    transitions = transitions_result.get("transitions", [])
    transition_id = None
    
    for transition in transitions:
        if transition.get("name").lower() == transition_name.lower():
            transition_id = transition.get("id")
            break
    
    if not transition_id:
        available = [t.get("name") for t in transitions]
        return f"Transition '{transition_name}' not found. Available transitions: {', '.join(available)}"
    
    # Execute the transition
    data = {
        "transition": {
            "id": transition_id
        }
    }
    
    result = await make_jira_request("POST", f"/rest/api/2/issue/{issue_key}/transitions", data)
    
    if "error" in result:
        return f"Error transitioning issue: {result.get('message', 'Unknown error')}"
    
    return f"Issue {issue_key} transitioned to '{transition_name}' successfully."

# === RESOURCES ===

@mcp.resource("jira://projects")
async def get_projects() -> str:
    """Get a list of all Jira projects."""
    result = await make_jira_request("GET", "/rest/api/2/project")
    
    if "error" in result:
        return f"Error retrieving projects: {result.get('message', 'Unknown error')}"
    
    projects = []
    for project in result:
        projects.append(f"{project.get('key')}: {project.get('name')}")
    
    return "\n".join(projects)

@mcp.resource("jira://issuetypes")
async def get_issue_types() -> str:
    """Get a list of all issue types."""
    result = await make_jira_request("GET", "/rest/api/2/issuetype")
    
    if "error" in result:
        return f"Error retrieving issue types: {result.get('message', 'Unknown error')}"
    
    issue_types = []
    for issue_type in result:
        issue_types.append(f"{issue_type.get('name')}: {issue_type.get('description', 'No description')}")
    
    return "\n".join(issue_types)

@mcp.resource("jira://priorities")
async def get_priorities() -> str:
    """Get a list of all priorities."""
    result = await make_jira_request("GET", "/rest/api/2/priority")
    
    if "error" in result:
        return f"Error retrieving priorities: {result.get('message', 'Unknown error')}"
    
    priorities = []
    for priority in result:
        priorities.append(f"{priority.get('name')}: {priority.get('description', 'No description')}")
    
    return "\n".join(priorities)

# === PROMPTS ===

@mcp.prompt("create_bug")
def create_bug_prompt(summary: str = None, steps: str = None, expected: str = None, actual: str = None):
    """
    A prompt template for creating a bug report.
    
    Args:
        summary: Brief description of the bug
        steps: Steps to reproduce
        expected: Expected behavior
        actual: Actual behavior
    """
    if all([summary, steps, expected, actual]):
        bug_description = f"""
*Steps to Reproduce:*
{steps}

*Expected Result:*
{expected}

*Actual Result:*
{actual}
        """
        
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please help me create a Jira bug report with the following details:\n\nSummary: {summary}\n\nDescription: {bug_description}"
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
                        "text": "I need to create a bug report in Jira. Please help me structure it with the following sections:\n\n- Summary\n- Steps to Reproduce\n- Expected Result\n- Actual Result"
                    }
                }
            ]
        }

@mcp.prompt("jql_search")
def jql_search_prompt(project: str = None, status: str = None, assignee: str = None, priority: str = None):
    """
    A prompt template for creating JQL search queries.
    
    Args:
        project: Project key
        status: Issue status
        assignee: Assignee username
        priority: Priority level
    """
    jql_parts = []
    
    if project:
        jql_parts.append(f"project = {project}")
    
    if status:
        jql_parts.append(f"status = \"{status}\"")
    
    if assignee:
        if assignee.lower() == "me":
            jql_parts.append("assignee = currentUser()")
        else:
            jql_parts.append(f"assignee = \"{assignee}\"")
    
    if priority:
        jql_parts.append(f"priority = \"{priority}\"")
    
    jql = " AND ".join(jql_parts) if jql_parts else ""
    
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"Please help me search for Jira issues using this JQL query:\n\n{jql}\n\nIf needed, help me refine it to find the right issues."
                }
            }
        ]
    }

if __name__ == "__main__":
    print("Starting Jira MCP server...", file=sys.stderr)
    mcp.run()