# Amplitude MCP Server

A Model Context Protocol (MCP) server for Amplitude integration. This server provides tools for interacting with Amplitude's analytics platform, including tracking events, retrieving analytics data, and managing dashboards.

## Features

- **Event Tracking**: Send events to Amplitude for tracking user behavior
- **User Analytics**: Retrieve user activity data and sessions
- **Dashboard Management**: List and get information about Amplitude dashboards
- **Cohort Management**: Access cohort information and data
- **Analytics Queries**: Run queries against Amplitude analytics data
- **Events Management**: Get information about tracked events

## Installation

```bash
pip install mcp-amplitude
```

## Configuration

Set the following environment variables:

```bash
export AMPLITUDE_BASE_URL="https://api.amplitude.com"  # Optional, default is already set
export AMPLITUDE_API_KEY="your_api_key"
export AMPLITUDE_SECRET_KEY="your_secret_key"  # Required for certain API calls like user exports
```

## Usage

### Starting the server directly

```bash
mcp-amplitude
```

### Using with Claude Desktop

Add the following to your `claude_desktop_config.json` file:

```json
"mcpServers": {
  "amplitude": {
    "command": "uvx",
    "args": [
      "mcp-amplitude"
    ],
    "env": {
      "AMPLITUDE_API_KEY": "your_api_key",
      "AMPLITUDE_SECRET_KEY": "your_secret_key"
    }
  }
}
```

Replace the environment variables with your actual Amplitude credentials.

### Using with uvx

```bash
uvx mcp-amplitude
```

With environment variables:

```bash
AMPLITUDE_API_KEY="your_api_key" AMPLITUDE_SECRET_KEY="your_secret_key" uvx mcp-amplitude
```

## Available Tools

* **send_event**: Send an event to Amplitude with user_id/device_id and properties
* **get_user_activity**: Get activity data for a specific user
* **query_chart**: Get data from a specific Amplitude chart
* **get_cohorts**: List available cohorts in your Amplitude account
* **get_dashboards**: List available dashboards in your Amplitude account
* **get_dashboard_details**: Get detailed information about a specific dashboard
* **get_events_list**: Get a list of all event types tracked in your Amplitude account

## Available Resources

* **amplitude://dashboards**: List of all dashboards in your Amplitude account
* **amplitude://events**: List of all event types in your Amplitude account
* **amplitude://cohorts**: List of all cohorts in your Amplitude account

## Available Prompts

* **analyze_user_behavior**: Template for analyzing user behavior patterns
* **create_dashboard**: Template for creating a new dashboard in Amplitude
* **track_conversion_funnel**: Template for analyzing conversion funnels

## Authentication

The Amplitude MCP server uses different authentication methods depending on the API endpoint:

1. **HTTP API & Batch API**: Uses the API key in the URL parameters
2. **Export API**: Uses Basic Authentication with API key and Secret key
3. **Dashboard & Management APIs**: Uses Bearer token authentication with the API key

Make sure you have set the appropriate environment variables before running the server.

## Version

0.0.1
