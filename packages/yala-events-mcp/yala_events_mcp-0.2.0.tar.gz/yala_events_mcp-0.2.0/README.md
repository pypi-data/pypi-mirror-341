# Yala Events MCP Server

A Model Context Protocol (MCP) server for Yala Events that provides access to events, organizations, roles, and other Yala Events API features.

## Installation

```bash
pip install yala-events-mcp
```

## Usage

### Command Line

1. Set up your environment variables in a `.env` file:

```env
YALA_EVENTS_API_TOKEN=your_api_token
BASE_URL=https://api.yala.events
```

2. Run the server in stdio mode:

```bash
yala-events-mcp
```

### Claude Desktop Configuration

Add this to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
"yala-events-mcp": {
  "command": "python3",
  "args": ["-m", "yala_events_mcp.server"],
  "env": {
    "YALA_EVENTS_API_TOKEN": "your_api_token",
    "BASE_URL": "https://api.yala.events"
  }
}
```

## Available Tools

- List Events
- Create Event
- Get Event Details
- Get Organizations
- List Histories
- List/Create/Update/Delete Modules
- List/Create/Update/Delete Permissions
- List/Create/Update/Delete Roles
- Manage Favorite Events
- Manage Personal Access Tokens
- List Public Organizations
- Get App Version
- Health Check

## License

MIT License
