import os
import sys
from typing import Any
import httpx
import logging
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Verify environment variables
API_TOKEN = os.getenv("YALA_EVENTS_API_TOKEN")
BASE_URL = os.getenv("BASE_URL")

if not API_TOKEN:
    logger.error("YALA_EVENTS_API_TOKEN environment variable not set")
    sys.exit(1)

# Create FastMCP server
mcp = FastMCP(
    name="Yala Events Server",
    host="0.0.0.0",
    port="3000",
    config={
        "sse": {
            "heartbeat_interval": 15,  # Send heartbeat every 15 seconds
            "retry_interval": 3000,    # Client retry after 3 seconds
            "cors": True,              # Enable CORS for SSE
            "cors_origins": ["*"],     # Allow all origins (you may want to restrict this)
            "keep_alive": True         # Enable keep-alive
        }
    }
)
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Helper function for API requests
async def make_api_request(method: str, url: str, json: dict = None, params: dict = None) -> dict[str, Any] | None:
    """Make a request to the yala.events API with error handling."""
    async with httpx.AsyncClient() as client:
        try:
            logger.info(f"Making {method} request to {url}")
            response = await client.request(
                method=method,
                url=url,
                headers=HEADERS,
                json=json,
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            logger.info(f"Successfully completed request to {url}")
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"API error: {e.response.status_code} - {e.response.text}")
            return {"error": f"API error: {e.response.status_code} - {e.response.text}"}
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            return {"error": f"Request failed: {str(e)}"}

# Tool 1: List Events
@mcp.tool()
async def list_events(date: str = None) -> str:
    """List events from yala.events with an optional date filter."""
    params = {"date": date} if date else {}
    data = await make_api_request("GET", f"{BASE_URL}/api/events", params=params)
    
    if not data or "data" not in data:
        logger.warning("No events data received")
        return "Unable to fetch events or no events found."
    
    if not data["data"]:
        return "No events found for this date."
    
    events = [f"Event: {event['title']} | Date: {event['startDateTime']} | ID: {event['id']}" 
              for event in data["data"]]
    return "\n---\n".join(events)

# Tool 2: Create Event
@mcp.tool()

async def create_event(title: str, content: str, date: str, organization_id: int, type_id: int, 
                      category_id: int, format_id: int, covers: list[str], is_private: bool) -> str:
    """Create a new event on yala.events."""
    payload = {
        "title": title,
        "content": content,
        "startDateTime": date,
        "typeId": type_id,
        "categoryId": category_id,
        "formatId": format_id,
        "covers": covers,
        "isPrivate": is_private
    }
    data = await make_api_request("POST", f"{BASE_URL}/api/events/organization/{organization_id}", json=payload)
    
    if not data or "data" not in data:
        logger.warning(f"Failed to create event: {data.get('error', 'Unknown error')}")
        return f"Failed to create event: {data.get('error', 'Unknown error')}"
    
    event = data["data"]
    logger.info(f"Created event: {event['title']} (ID: {event['id']})")
    return f"Event created: {event['title']} (ID: {event['id']})"

# Tool 3: Get Event Details
@mcp.tool()
async def get_event_details(event_id: int) -> str:
    """Get detailed information about a specific event."""
    data = await make_api_request("GET", f"{BASE_URL}/api/events/{event_id}")
    
    if not data or "data" not in data:
        logger.warning(f"Failed to fetch event details: {data.get('error', 'Event not found')}")
        return f"Unable to fetch event details: {data.get('error', 'Event not found')}"
    
    event = data["data"]
    details = [
        f"Title: {event['title']}",
        f"ID: {event['id']}",
        f"Date: {event['startDateTime']}",
        f"Content: {event['content']}",
        f"Private: {event['isPrivate']}",
        f"Organization ID: {event['organizationId']}",
        f"Covers: {', '.join(event['covers'])}"
        
    ]
    return "\n".join(details)

# Tool 4: Get Organizations
@mcp.tool()
async def get_organizations() -> str:
    """List all organizations on yala.events."""
    data = await make_api_request("GET", f"{BASE_URL}/api/organizations")
    
    if not data or "data" not in data:
        logger.warning("No organizations data received")
        return "Unable to fetch organizations or no organizations found."
    
    if not data["data"]:
        return "No organizations found."
    
    orgs = [f"Organization: {org['name']} | ID: {org['id']}" for org in data["data"]]
    return "\n---\n".join(orgs)

# Tool 5: List Histories
@mcp.tool()
async def list_histories(limit: int = None, page: int = None) -> str:
    """List history records from yala.events."""
    params = {}
    if limit: params["limit"] = limit
    if page: params["page"] = page
    
    data = await make_api_request("GET", f"{BASE_URL}/api/histories", params=params)
    
    if not data or "data" not in data:
        return "Unable to fetch histories or no histories found."
    
    if not data["data"]:
        return "No history records found."
    
    histories = [f"ID: {h['id']} | Module: {h['module']} | Action: {h['action']} | Date: {h['createdAt']}" 
                 for h in data["data"]]
    return "\n---\n".join(histories)

# Tool 6: List Modules
@mcp.tool()
async def list_modules(search: str = None) -> str:
    """List modules from yala.events with optional search."""
    params = {"search": search} if search else {}
    data = await make_api_request("GET", f"{BASE_URL}/api/modules", params=params)
    
    if not data or "data" not in data:
        return "Unable to fetch modules or no modules found."
    
    if not data["data"]:
        return "No modules found."
    
    modules = [f"Module: {m['name']} | ID: {m['id']}" for m in data["data"]]
    return "\n---\n".join(modules)

# Tool 7: Create Module
@mcp.tool()
async def create_module(name: str) -> str:
    """Create a new module on yala.events."""
    payload = {"name": name}
    data = await make_api_request("POST", f"{BASE_URL}/api/modules", json=payload)
    
    if not data or "data" not in data:
        return f"Failed to create module: {data.get('error', 'Unknown error')}"
    
    module = data["data"]
    return f"Module created: {module['name']} (ID: {module['id']})"

# Tool 8: Update Module
@mcp.tool()
async def update_module(module_id: int, name: str) -> str:
    """Update an existing module."""
    payload = {"name": name}
    data = await make_api_request("PUT", f"{BASE_URL}/api/modules/{module_id}", json=payload)
    
    if not data or "data" not in data:
        return f"Failed to update module: {data.get('error', 'Unknown error')}"
    
    module = data["data"]
    return f"Module updated: {module['name']} (ID: {module['id']})"

# Tool 9: Delete Module
@mcp.tool()
async def delete_module(module_id: int) -> str:
    """Delete a module."""
    data = await make_api_request("DELETE", f"{BASE_URL}/api/modules/{module_id}")
    
    if not data or "data" not in data:
        return f"Failed to delete module: {data.get('error', 'Unknown error')}"
    
    return f"Module deleted (ID: {module_id})"

# Tool 10: Get Module Histories
@mcp.tool()
async def get_module_histories(limit: int = None, page: int = None) -> str:
    """Get history records for modules."""
    params = {}
    if limit: params["limit"] = limit
    if page: params["page"] = page
    
    data = await make_api_request("GET", f"{BASE_URL}/api/modules/histories", params=params)
    
    if not data or "data" not in data:
        return "Unable to fetch module histories."
    
    histories = [f"ID: {h['id']} | Module: {h['module']} | Action: {h['action']}" for h in data["data"]]
    return "\n---\n".join(histories)

# Tool 11: List Permissions
@mcp.tool()
async def list_permissions(search: str = None) -> str:
    """List permissions from yala.events."""
    params = {"search": search} if search else {}
    data = await make_api_request("GET", f"{BASE_URL}/api/permissions", params=params)
    
    if not data or "data" not in data:
        return "Unable to fetch permissions."
    
    perms = [f"Permission: {p['name']} | ID: {p['id']}" for p in data["data"]]
    return "\n---\n".join(perms)

# Tool 12: Create Permission
@mcp.tool()
async def create_permission(name: str) -> str:
    """Create a new permission."""
    payload = {"name": name}
    data = await make_api_request("POST", f"{BASE_URL}/api/permissions", json=payload)
    
    if not data or "data" not in data:
        return f"Failed to create permission: {data.get('error', 'Unknown error')}"
    
    perm = data["data"]
    return f"Permission created: {perm['name']} (ID: {perm['id']})"

# Tool 13: Update Permission
@mcp.tool()
async def update_permission(permission_id: int, name: str) -> str:
    """Update an existing permission."""
    payload = {"name": name}
    data = await make_api_request("PUT", f"{BASE_URL}/api/permissions/{permission_id}", json=payload)
    
    if not data or "data" not in data:
        return f"Failed to update permission: {data.get('error', 'Unknown error')}"
    
    perm = data["data"]
    return f"Permission updated: {perm['name']} (ID: {perm['id']})"

# Tool 14: Delete Permission
@mcp.tool()
async def delete_permission(permission_id: int) -> str:
    """Delete a permission."""
    data = await make_api_request("DELETE", f"{BASE_URL}/api/permissions/{permission_id}")
    
    if not data or "data" not in data:
        return f"Failed to delete permission: {data.get('error', 'Unknown error')}"
    
    return f"Permission deleted (ID: {permission_id})"

# Tool 15: Get Permission Histories
@mcp.tool()
async def get_permission_histories(limit: int = None, page: int = None) -> str:
    """Get history records for permissions."""
    params = {}
    if limit: params["limit"] = limit
    if page: params["page"] = page
    
    data = await make_api_request("GET", f"{BASE_URL}/api/permissions/histories", params=params)
    
    if not data or "data" not in data:
        return "Unable to fetch permission histories."
    
    histories = [f"ID: {h['id']} | Module: {h['module']} | Action: {h['action']}" for h in data["data"]]
    return "\n---\n".join(histories)

# Tool 16: List Roles
@mcp.tool()
async def list_roles(search: str = None) -> str:
    """List roles from yala.events."""
    params = {"search": search} if search else {}
    data = await make_api_request("GET", f"{BASE_URL}/api/roles", params=params)
    
    if not data or "data" not in data:
        return "Unable to fetch roles."
    
    roles = [f"Role: {r['name']} | ID: {r['id']} | Users: {r['_count']['users']}" for r in data["data"]]
    return "\n---\n".join(roles)

# Tool 17: Create Role
@mcp.tool()
async def create_role(name: str, permissions_per_module: list[dict]) -> str:
    """Create a new role with permissions per module."""
    payload = {
        "name": name,
        "permissionsPerModule": permissions_per_module  # List of {"moduleId": int, "permissionId": int}
    }
    data = await make_api_request("POST", f"{BASE_URL}/api/roles", json=payload)
    
    if not data or "data" not in data:
        return f"Failed to create role: {data.get('error', 'Unknown error')}"
    
    role = data["data"]
    return f"Role created: {role['name']} (ID: {role['id']})"

# Tool 18: Update Role
@mcp.tool()
async def update_role(role_id: int, name: str, permissions_per_module: list[dict]) -> str:
    """Update an existing role."""
    payload = {
        "name": name,
        "permissionsPerModule": permissions_per_module
    }
    data = await make_api_request("PUT", f"{BASE_URL}/api/roles/{role_id}", json=payload)
    
    if not data or "data" not in data:
        return f"Failed to update role: {data.get('error', 'Unknown error')}"
    
    role = data["data"]
    return f"Role updated: {role['name']} (ID: {role['id']})"

# Tool 19: Delete Role
@mcp.tool()
async def delete_role(role_id: int) -> str:
    """Delete a role."""
    data = await make_api_request("DELETE", f"{BASE_URL}/api/roles/{role_id}")
    
    if not data or "data" not in data:
        return f"Failed to delete role: {data.get('error', 'Unknown error')}"
    
    return f"Role deleted (ID: {role_id})"

# Tool 20: Get Role Histories
@mcp.tool()
async def get_role_histories(limit: int = None, page: int = None) -> str:
    """Get history records for roles."""
    params = {}
    if limit: params["limit"] = limit
    if page: params["page"] = page
    
    data = await make_api_request("GET", f"{BASE_URL}/api/roles/histories", params=params)
    
    if not data or "data" not in data:
        return "Unable to fetch role histories."
    
    histories = [f"ID: {h['id']} | Module: {h['module']} | Action: {h['action']}" for h in data["data"]]
    return "\n---\n".join(histories)

# Tool 21: List Favorites Events
@mcp.tool()
async def list_favorites_events() -> str:
    """List favorite events."""
    data = await make_api_request("GET", f"{BASE_URL}/api/favorites-events")
    
    if not data or "data" not in data:
        return "Unable to fetch favorite events."
    
    favorites = [f"Event: {f['event']['title']} | User: {f['user']['firstName']} {f['user']['lastName']} | ID: {f['id']}" 
                 for f in data["data"]]
    return "\n---\n".join(favorites)

# Tool 22: Create Favorite Event
@mcp.tool()
async def create_favorite_event(event_id: int, user_id: int) -> str:
    """Add an event to favorites."""
    payload = {"eventId": event_id, "userId": user_id}
    data = await make_api_request("POST", f"{BASE_URL}/api/favorites-events", json=payload)
    
    if not data or "data" not in data:
        return f"Failed to create favorite: {data.get('error', 'Unknown error')}"
    
    favorite = data["data"]
    return f"Favorite created for event ID: {favorite['eventId']}"

# Tool 23: Update Favorite Event
@mcp.tool()
async def update_favorite_event(favorite_id: int, event_id: int, user_id: int) -> str:
    """Update a favorite event."""
    payload = {"eventId": event_id, "userId": user_id}
    data = await make_api_request("PUT", f"{BASE_URL}/api/favorites-events/{favorite_id}", json=payload)
    
    if not data or "data" not in data:
        return f"Failed to update favorite: {data.get('error', 'Unknown error')}"
    
    return f"Favorite updated (ID: {favorite_id})"

# Tool 24: Delete Favorite Event
@mcp.tool()
async def delete_favorite_event(favorite_id: int) -> str:
    """Remove an event from favorites."""
    data = await make_api_request("DELETE", f"{BASE_URL}/api/favorites-events/{favorite_id}")
    
    if not data or "data" not in data:
        return f"Failed to delete favorite: {data.get('error', 'Unknown error')}"
    
    return f"Favorite deleted (ID: {favorite_id})"

# Tool 25: Get Favorites Events Histories
@mcp.tool()
async def get_favorites_events_histories(limit: int = None, page: int = None) -> str:
    """Get history records for favorite events."""
    params = {}
    if limit: params["limit"] = limit
    if page: params["page"] = page
    
    data = await make_api_request("GET", f"{BASE_URL}/api/favorites-events/histories", params=params)
    
    if not data or "data" not in data:
        return "Unable to fetch favorites histories."
    
    histories = [f"ID: {h['id']} | Module: {h['module']} | Action: {h['action']}" for h in data["data"]]
    return "\n---\n".join(histories)

# Tool 26: List Personal Access Tokens
@mcp.tool()
async def list_personal_access_tokens(search: str = None) -> str:
    """List personal access tokens."""
    params = {"search": search} if search else {}
    data = await make_api_request("GET", f"{BASE_URL}/api/personals-accesses-tokens", params=params)
    
    if not data or "data" not in data:
        return "Unable to fetch personal access tokens."
    
    tokens = [f"Name: {t['name']} | ID: {t['id']} | Expires: {t.get('expireAt', 'Never')}" for t in data["data"]]
    return "\n---\n".join(tokens)

# Tool 27: Create Personal Access Token
@mcp.tool()
async def create_personal_access_token(name: str, expire: bool, expire_at: str = None) -> str:
    """Create a new personal access token."""
    payload = {"name": name, "expire": expire}
    if expire_at:
        payload["expireAt"] = expire_at
    
    data = await make_api_request("POST", f"{BASE_URL}/api/personals-accesses-tokens", json=payload)
    
    if not data or "data" not in data:
        return f"Failed to create token: {data.get('error', 'Unknown error')}"
    
    return f"Token created: {data['data']}"

# Tool 28: Update Personal Access Token
@mcp.tool()
async def update_personal_access_token(token_id: int, name: str, expire: bool, expire_at: str = None) -> str:
    """Update a personal access token."""
    payload = {"name": name, "expire": expire}
    if expire_at:
        payload["expireAt"] = expire_at
    
    data = await make_api_request("PUT", f"{BASE_URL}/api/personals-accesses-tokens/{token_id}", json=payload)
    
    if not data or "data" not in data:
        return f"Failed to update token: {data.get('error', 'Unknown error')}"
    
    token = data["data"]
    return f"Token updated: {token['name']} (ID: {token['id']})"

# Tool 29: Delete Personal Access Token
@mcp.tool()
async def delete_personal_access_token(token_id: int) -> str:
    """Delete a personal access token."""
    data = await make_api_request("DELETE", f"{BASE_URL}/api/personals-accesses-tokens/{token_id}")
    
    if not data or "data" not in data:
        return f"Failed to delete token: {data.get('error', 'Unknown error')}"
    
    return f"Token deleted (ID: {token_id})"

# Tool 30: Get Personal Access Token Histories
@mcp.tool()
async def get_personal_access_token_histories(limit: int = None, page: int = None) -> str:
    """Get history records for personal access tokens."""
    params = {}
    if limit: params["limit"] = limit
    if page: params["page"] = page
    
    data = await make_api_request("GET", f"{BASE_URL}/api/personals-accesses-tokens/histories", params=params)
    
    if not data or "data" not in data:
        return "Unable to fetch token histories."
    
    histories = [f"ID: {h['id']} | Module: {h['module']} | Action: {h['action']}" for h in data["data"]]
    return "\n---\n".join(histories)

# Tool 31: List Public Organizations (SEO)
@mcp.tool()
async def list_public_organizations(search: str = None) -> str:
    """List public organizations for SEO purposes."""
    params = {"search": search} if search else {}
    data = await make_api_request("GET", f"{BASE_URL}/api/seo/organizations/public", params=params)
    
    if not data or "data" not in data:
        return "Unable to fetch public organizations."
    
    orgs = [f"Name: {o['name']} | ID: {o['id']} | Slug: {o['slug']}" for o in data["data"]]
    return "\n---\n".join(orgs)

# Tool 32: Get App Version
@mcp.tool()
async def get_app_version() -> str:
    """Get the application version information."""
    data = await make_api_request("GET", f"{BASE_URL}/app/info/version")
    
    if not data:
        return "Unable to fetch version information."
    
    return f"App Name: {data['name']} | Version: {data['version']}"

# Tool 33: Health Check
@mcp.tool()
async def health_check() -> str:
    """Perform a health check on the application."""
    data = await make_api_request("GET", f"{BASE_URL}/app/info/health-check")
    
    if not data:
        return "Health check failed."
    
    return "Application is healthy."

if __name__ == "__main__":
    logger.info("Starting Yala Events MCP server with see transport...")
    mcp.run(transport="sse")