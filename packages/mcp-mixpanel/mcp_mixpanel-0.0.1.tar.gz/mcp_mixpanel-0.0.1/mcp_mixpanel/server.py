# server.py
import sys
import os
import json
from typing import Dict, List, Optional, Any, Union
import httpx
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Mixpanel MCP")

# Environment variables for Mixpanel configuration
MIXPANEL_API_SECRET = os.environ.get("MIXPANEL_API_SECRET")
MIXPANEL_PROJECT_ID = os.environ.get("MIXPANEL_PROJECT_ID")
MIXPANEL_SERVICE_ACCOUNT_USERNAME = os.environ.get("MIXPANEL_SERVICE_ACCOUNT_USERNAME")
MIXPANEL_SERVICE_ACCOUNT_PASSWORD = os.environ.get("MIXPANEL_SERVICE_ACCOUNT_PASSWORD")

# Base URLs for different Mixpanel APIs
MIXPANEL_API_URL = "https://api.mixpanel.com"
MIXPANEL_EU_API_URL = "https://api-eu.mixpanel.com"
MIXPANEL_DATA_API_URL = "https://data.mixpanel.com/api/2.0"

# Check if environment variables are set
if not MIXPANEL_API_SECRET:
    print("Warning: Mixpanel environment variables not fully configured. Set MIXPANEL_API_SECRET.", file=sys.stderr)

# Helper function for API requests
async def make_mixpanel_request(method: str, endpoint: str, api_type: str = "main", data: Dict = None, params: Dict = None) -> Dict:
    """
    Make a request to the Mixpanel API.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint (without base URL)
        api_type: Type of API to use (main, eu, data)
        data: Data to send (for POST/PUT)
        params: Query parameters
    
    Returns:
        Response from Mixpanel API as dictionary
    """
    # Select the appropriate base URL based on the API type
    base_url = MIXPANEL_API_URL
    if api_type == "eu":
        base_url = MIXPANEL_EU_API_URL
    elif api_type == "data":
        base_url = MIXPANEL_DATA_API_URL
    
    url = f"{base_url}{endpoint}"
    
    # Determine authentication method
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    auth = None
    
    if MIXPANEL_API_SECRET:
        # Use API secret for authentication
        headers["Authorization"] = f"Bearer {MIXPANEL_API_SECRET}"
    elif MIXPANEL_SERVICE_ACCOUNT_USERNAME and MIXPANEL_SERVICE_ACCOUNT_PASSWORD:
        # Use service account credentials
        auth = (MIXPANEL_SERVICE_ACCOUNT_USERNAME, MIXPANEL_SERVICE_ACCOUNT_PASSWORD)
    
    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, params=params, auth=auth, timeout=30.0)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=data, params=params, auth=auth, timeout=30.0)
            elif method.upper() == "PUT":
                response = await client.put(url, headers=headers, json=data, params=params, auth=auth, timeout=30.0)
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers, params=params, auth=auth, timeout=30.0)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            
            # Handle empty responses
            if not response.text or response.text.isspace():
                return {"success": True}
            
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": True,
                "status_code": e.response.status_code,
                "message": e.response.text
            }
        except Exception as e:
            return {
                "error": True,
                "message": str(e)
            }

# === TOOLS ===

@mcp.tool()
async def query_events(event_name: str, from_date: str, to_date: str, limit: int = 100) -> str:
    """
    Query Mixpanel events.
    
    Args:
        event_name: Name of the event to query
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
        limit: Maximum number of results to return (default: 100)
    """
    params = {
        "event": json.dumps([event_name]),
        "from_date": from_date,
        "to_date": to_date,
        "limit": limit
    }
    
    if MIXPANEL_PROJECT_ID:
        params["project_id"] = MIXPANEL_PROJECT_ID
    
    result = await make_mixpanel_request("GET", "/api/2.0/events", params=params)
    
    if "error" in result:
        return f"Error querying events: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_user_profile(distinct_id: str) -> str:
    """
    Get a user profile from Mixpanel.
    
    Args:
        distinct_id: The distinct ID of the user
    """
    endpoint = f"/engage?distinct_id={distinct_id}"
    if MIXPANEL_PROJECT_ID:
        endpoint += f"&project_id={MIXPANEL_PROJECT_ID}"
    
    result = await make_mixpanel_request("GET", endpoint)
    
    if "error" in result:
        return f"Error retrieving user profile: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.tool()
async def create_annotation(date: str, description: str) -> str:
    """
    Create an annotation in Mixpanel.
    
    Args:
        date: Date for the annotation in YYYY-MM-DD format
        description: Description of the annotation
    """
    data = {
        "date": date,
        "description": description
    }
    
    if MIXPANEL_PROJECT_ID:
        data["project_id"] = MIXPANEL_PROJECT_ID
    
    result = await make_mixpanel_request("POST", "/api/2.0/annotations", data=data)
    
    if "error" in result:
        return f"Error creating annotation: {result.get('message', 'Unknown error')}"
    
    return f"Annotation created successfully for {date}: {description}"

@mcp.tool()
async def get_funnel_data(funnel_id: str, from_date: str, to_date: str) -> str:
    """
    Get funnel data from Mixpanel.
    
    Args:
        funnel_id: ID of the funnel
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
    """
    params = {
        "funnel_id": funnel_id,
        "from_date": from_date,
        "to_date": to_date
    }
    
    if MIXPANEL_PROJECT_ID:
        params["project_id"] = MIXPANEL_PROJECT_ID
    
    result = await make_mixpanel_request("GET", "/api/2.0/funnels", params=params)
    
    if "error" in result:
        return f"Error retrieving funnel data: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_cohorts() -> str:
    """
    Get a list of cohorts from Mixpanel.
    """
    params = {}
    if MIXPANEL_PROJECT_ID:
        params["project_id"] = MIXPANEL_PROJECT_ID
    
    result = await make_mixpanel_request("GET", "/api/2.0/cohorts/list", params=params)
    
    if "error" in result:
        return f"Error retrieving cohorts: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.tool()
async def export_events(from_date: str, to_date: str, event: str = None) -> str:
    """
    Export raw event data from Mixpanel.
    
    Args:
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
        event: Optional name of the specific event to export (default: all events)
    """
    params = {
        "from_date": from_date,
        "to_date": to_date
    }
    
    if event:
        params["event"] = [event]
    
    if MIXPANEL_PROJECT_ID:
        params["project_id"] = MIXPANEL_PROJECT_ID
    
    result = await make_mixpanel_request("GET", "/export", api_type="data", params=params)
    
    if "error" in result:
        return f"Error exporting events: {result.get('message', 'Unknown error')}"
    
    # Limit the output size for readability
    return json.dumps(result[:100] if isinstance(result, list) else result, indent=2)

# === RESOURCES ===

@mcp.resource("mixpanel://events")
async def get_event_names() -> str:
    """Get a list of all event names in Mixpanel."""
    params = {}
    if MIXPANEL_PROJECT_ID:
        params["project_id"] = MIXPANEL_PROJECT_ID
    
    result = await make_mixpanel_request("GET", "/api/2.0/events/names", params=params)
    
    if "error" in result:
        return f"Error retrieving event names: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.resource("mixpanel://properties")
async def get_event_properties() -> str:
    """Get a list of all event properties in Mixpanel."""
    params = {}
    if MIXPANEL_PROJECT_ID:
        params["project_id"] = MIXPANEL_PROJECT_ID
    
    result = await make_mixpanel_request("GET", "/api/2.0/events/properties", params=params)
    
    if "error" in result:
        return f"Error retrieving event properties: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.resource("mixpanel://funnels")
async def get_funnels() -> str:
    """Get a list of all funnels in Mixpanel."""
    params = {}
    if MIXPANEL_PROJECT_ID:
        params["project_id"] = MIXPANEL_PROJECT_ID
    
    result = await make_mixpanel_request("GET", "/api/2.0/funnels/list", params=params)
    
    if "error" in result:
        return f"Error retrieving funnels: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.resource("mixpanel://annotations")
async def get_annotations() -> str:
    """Get a list of all annotations in Mixpanel."""
    params = {}
    if MIXPANEL_PROJECT_ID:
        params["project_id"] = MIXPANEL_PROJECT_ID
    
    result = await make_mixpanel_request("GET", "/api/2.0/annotations", params=params)
    
    if "error" in result:
        return f"Error retrieving annotations: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

# === PROMPTS ===

@mcp.prompt("query_events")
def query_events_prompt(event_name: str = None, from_date: str = None, to_date: str = None):
    """
    A prompt template for querying Mixpanel events.
    
    Args:
        event_name: Name of the event to query
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
    """
    if all([event_name, from_date, to_date]):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please analyze the Mixpanel event data for '{event_name}' between {from_date} and {to_date}. What patterns, trends, or insights can you identify?"
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
                        "text": "I want to analyze some Mixpanel event data. Please help me formulate a query with the appropriate event name and date range."
                    }
                }
            ]
        }

@mcp.prompt("funnel_analysis")
def funnel_analysis_prompt(funnel_id: str = None, from_date: str = None, to_date: str = None):
    """
    A prompt template for analyzing funnel data.
    
    Args:
        funnel_id: ID of the funnel
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
    """
    if all([funnel_id, from_date, to_date]):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please analyze the funnel with ID '{funnel_id}' from {from_date} to {to_date}. What are the conversion rates at each step? Where do we see the biggest drop-offs? What recommendations can you provide to improve the funnel performance?"
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
                        "text": "I want to analyze a Mixpanel funnel. Please help me identify which funnel to examine and the appropriate date range for the analysis."
                    }
                }
            ]
        }

@mcp.prompt("create_annotation")
def create_annotation_prompt(date: str = None, description: str = None):
    """
    A prompt template for creating a Mixpanel annotation.
    
    Args:
        date: Date for the annotation in YYYY-MM-DD format
        description: Description of the annotation
    """
    if all([date, description]):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"I'd like to create a Mixpanel annotation for {date} with the description: \"{description}\". Could you help me with that?"
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
                        "text": "I want to create a Mixpanel annotation to mark an important event or change. Please help me specify the date and description for this annotation."
                    }
                }
            ]
        }

if __name__ == "__main__":
    print("Starting Mixpanel MCP server...", file=sys.stderr)
    mcp.run()
