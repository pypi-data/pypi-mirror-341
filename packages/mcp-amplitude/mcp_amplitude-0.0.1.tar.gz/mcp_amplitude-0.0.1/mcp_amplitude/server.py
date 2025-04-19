
# server.py
import sys
import os
import json
from typing import Dict, List, Optional, Any, Union
import httpx
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Amplitude MCP")

# Environment variables for Amplitude configuration
AMPLITUDE_BASE_URL = os.environ.get("AMPLITUDE_BASE_URL", "https://api.amplitude.com")
AMPLITUDE_API_KEY = os.environ.get("AMPLITUDE_API_KEY")
AMPLITUDE_SECRET_KEY = os.environ.get("AMPLITUDE_SECRET_KEY")

# Check if environment variables are set
if not all([AMPLITUDE_API_KEY, AMPLITUDE_SECRET_KEY]):
    print("Warning: Amplitude environment variables not fully configured. Set AMPLITUDE_API_KEY and AMPLITUDE_SECRET_KEY.", file=sys.stderr)

# Helper function for API requests
async def make_amplitude_request(method: str, endpoint: str, data: Dict = None) -> Dict:
    """
    Make a request to the Amplitude API.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint (without base URL)
        data: Data to send (for POST/PUT)
    
    Returns:
        Response from Amplitude API as dictionary
    """
    url = f"{AMPLITUDE_BASE_URL}{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Authentication depending on the endpoint
    auth = None
    if "/export" in endpoint:
        # For data export APIs, use API key and Secret key
        auth = (AMPLITUDE_API_KEY, AMPLITUDE_SECRET_KEY)
    elif "/batch" in endpoint or "/httpapi" in endpoint:
        # For event APIs, use API key in the URL
        if "?" in url:
            url += f"&api_key={AMPLITUDE_API_KEY}"
        else:
            url += f"?api_key={AMPLITUDE_API_KEY}"
    else:
        # For other APIs, use Bearer token authentication
        headers["Authorization"] = f"Bearer {AMPLITUDE_API_KEY}"
    
    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, auth=auth, timeout=30.0)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=data, auth=auth, timeout=30.0)
            elif method.upper() == "PUT":
                response = await client.put(url, headers=headers, json=data, auth=auth, timeout=30.0)
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers, auth=auth, timeout=30.0)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            
            # For some endpoints, the response might be CSV or other formats
            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                return response.json()
            else:
                return {"data": response.text, "content_type": content_type}
                
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
async def send_event(event_type: str, user_id: str = None, device_id: str = None, 
                     event_properties: Dict = None, user_properties: Dict = None) -> str:
    """
    Send an event to Amplitude.
    
    Args:
        event_type: The name of the event
        user_id: User ID for the event (either user_id or device_id is required)
        device_id: Device ID for the event (either user_id or device_id is required)
        event_properties: Additional properties related to the event
        user_properties: Properties to update on the user profile
    """
    if not user_id and not device_id:
        return "Error: Either user_id or device_id is required"
    
    event_data = {
        "api_key": AMPLITUDE_API_KEY,
        "events": [{
            "event_type": event_type,
            "time": int(1000 * __import__('time').time()),  # Current time in milliseconds
        }]
    }
    
    # Add optional parameters if provided
    if user_id:
        event_data["events"][0]["user_id"] = user_id
    if device_id:
        event_data["events"][0]["device_id"] = device_id
    if event_properties:
        event_data["events"][0]["event_properties"] = event_properties
    if user_properties:
        event_data["events"][0]["user_properties"] = user_properties
    
    result = await make_amplitude_request("POST", "/2/httpapi", event_data)
    
    if "error" in result:
        return f"Error sending event: {result.get('message', 'Unknown error')}"
    
    return "Event sent successfully"

@mcp.tool()
async def get_user_activity(user_id: str, start_date: str, end_date: str) -> str:
    """
    Get user activity from Amplitude.
    
    Args:
        user_id: The user ID to fetch activity for
        start_date: Start date (YYYYMMDD format)
        end_date: End date (YYYYMMDD format)
    """
    # Check if the export API is supported (needs both API key and Secret key)
    if not AMPLITUDE_SECRET_KEY:
        return "Error: AMPLITUDE_SECRET_KEY is required for user activity exports"
    
    params = f"?user={user_id}&start={start_date}&end={end_date}"
    result = await make_amplitude_request("GET", f"/api/2/useractivity{params}", None)
    
    if "error" in result:
        return f"Error retrieving user activity: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    if isinstance(result, dict):
        return json.dumps(result, indent=2)
    return str(result)

@mcp.tool()
async def query_chart(chart_id: str) -> str:
    """
    Get data from an Amplitude chart.
    
    Args:
        chart_id: The ID of the chart/dashboard item
    """
    result = await make_amplitude_request("GET", f"/api/3/chart/{chart_id}/query", None)
    
    if "error" in result:
        return f"Error retrieving chart data: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_cohorts() -> str:
    """
    Get a list of all cohorts in Amplitude.
    """
    result = await make_amplitude_request("GET", "/api/3/cohorts", None)
    
    if "error" in result:
        return f"Error retrieving cohorts: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_dashboards() -> str:
    """
    Get a list of all dashboards in Amplitude.
    """
    result = await make_amplitude_request("GET", "/api/3/dashboards", None)
    
    if "error" in result:
        return f"Error retrieving dashboards: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_dashboard_details(dashboard_id: str) -> str:
    """
    Get details of a specific Amplitude dashboard.
    
    Args:
        dashboard_id: The dashboard ID
    """
    result = await make_amplitude_request("GET", f"/api/3/dashboards/{dashboard_id}", None)
    
    if "error" in result:
        return f"Error retrieving dashboard details: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_events_list() -> str:
    """
    Get a list of all event types in Amplitude.
    """
    result = await make_amplitude_request("GET", "/api/2/events/list", None)
    
    if "error" in result:
        return f"Error retrieving events list: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

# === RESOURCES ===

@mcp.resource("amplitude://dashboards")
async def list_dashboards() -> str:
    """Get a list of all Amplitude dashboards."""
    result = await make_amplitude_request("GET", "/api/3/dashboards", None)
    
    if "error" in result:
        return f"Error retrieving dashboards: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.resource("amplitude://events")
async def list_events() -> str:
    """Get a list of all event types in Amplitude."""
    result = await make_amplitude_request("GET", "/api/2/events/list", None)
    
    if "error" in result:
        return f"Error retrieving events: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.resource("amplitude://cohorts")
async def list_cohorts() -> str:
    """Get a list of all cohorts in Amplitude."""
    result = await make_amplitude_request("GET", "/api/3/cohorts", None)
    
    if "error" in result:
        return f"Error retrieving cohorts: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

# === PROMPTS ===

@mcp.prompt("analyze_user_behavior")
def analyze_user_behavior_prompt(user_id: str = None, event_type: str = None, date_range: str = None):
    """
    A prompt template for analyzing user behavior in Amplitude.
    
    Args:
        user_id: ID of the user to analyze
        event_type: Specific event type to focus on
        date_range: Date range for the analysis (e.g., "last 7 days")
    """
    content = "I need to analyze user behavior in our Amplitude data."
    
    if user_id:
        content += f"\n\nPlease focus on user ID: {user_id}"
    
    if event_type:
        content += f"\n\nI'm particularly interested in the '{event_type}' event."
    
    if date_range:
        content += f"\n\nPlease analyze data from {date_range}."
    
    content += "\n\nCan you help me understand patterns, anomalies, or insights from this data?"
    
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": content
                }
            }
        ]
    }

@mcp.prompt("create_dashboard")
def create_dashboard_prompt(name: str = None, description: str = None, metrics: str = None):
    """
    A prompt template for creating a new dashboard in Amplitude.
    
    Args:
        name: Name of the dashboard
        description: Description of the dashboard
        metrics: Key metrics to include in the dashboard
    """
    content = "I want to create a new dashboard in Amplitude."
    
    if name:
        content += f"\n\nDashboard name: {name}"
    
    if description:
        content += f"\n\nDescription: {description}"
    
    if metrics:
        content += f"\n\nKey metrics to include: {metrics}"
    
    content += "\n\nCan you help me plan this dashboard and suggest the best charts and metrics to include?"
    
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": content
                }
            }
        ]
    }

@mcp.prompt("track_conversion_funnel")
def track_conversion_funnel_prompt(funnel_steps: str = None, start_date: str = None, end_date: str = None):
    """
    A prompt template for analyzing a conversion funnel in Amplitude.
    
    Args:
        funnel_steps: The steps in the conversion funnel
        start_date: Start date for the analysis
        end_date: End date for the analysis
    """
    content = "I need to analyze a conversion funnel in our Amplitude data."
    
    if funnel_steps:
        content += f"\n\nFunnel steps: {funnel_steps}"
    
    if start_date and end_date:
        content += f"\n\nTime period: {start_date} to {end_date}"
    
    content += "\n\nPlease help me understand conversion rates, drop-offs, and potential improvements."
    
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": content
                }
            }
        ]
    }

if __name__ == "__main__":
    print("Starting Amplitude MCP server...", file=sys.stderr)
    mcp.run()
