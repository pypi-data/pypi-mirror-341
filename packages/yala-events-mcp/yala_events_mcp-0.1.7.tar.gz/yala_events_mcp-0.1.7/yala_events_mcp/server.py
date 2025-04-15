import os
import sys
import logging
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from .api import YalaEventsAPI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_server() -> FastMCP:
    """Create and configure the MCP server."""
    # Load environment variables
    load_dotenv()

    # Verify environment variables
    api_token = os.getenv("YALA_EVENTS_API_TOKEN")
    base_url = os.getenv("BASE_URL")

    if not api_token:
        logger.error("YALA_EVENTS_API_TOKEN environment variable not set")
        sys.exit(1)

    if not base_url:
        logger.error("BASE_URL environment variable not set")
        sys.exit(1)

    # Create API client
    api = YalaEventsAPI(api_token, base_url)

    # Create MCP server
    mcp = FastMCP("Yala Events Server")

    # Event Tools
    @mcp.tool()
    async def list_events(date: str = None) -> str:
        """List events from yala.events with an optional date filter."""
        params = {"date": date} if date else {}
        data = await api.make_request("GET", f"{base_url}/api/events", params=params)
        
        if not data or "data" not in data:
            logger.warning("No events data received")
            return "Unable to fetch events or no events found."
        
        if not data["data"]:
            return "No events found for this date."
        
        events = [f"Event: {event['title']} | Date: {event['startDateTime']} | ID: {event['id']}" 
                  for event in data["data"]]
        return "\n---\n".join(events)

    @mcp.tool()
    async def create_event(
        title: str, 
        content: str, 
        date: str, 
        organization_id: int, 
        type_id: int,
        category_id: int, 
        format_id: int, 
        covers: list[str], 
        is_private: bool
    ) -> str:
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
        data = await api.make_request(
            "POST", 
            f"{base_url}/api/events/organization/{organization_id}", 
            json=payload
        )
        
        if not data or "data" not in data:
            logger.warning(f"Failed to create event: {data.get('error', 'Unknown error')}")
            return f"Failed to create event: {data.get('error', 'Unknown error')}"
        
        event = data["data"]
        logger.info(f"Created event: {event['title']} (ID: {event['id']})")
        return f"Event created: {event['title']} (ID: {event['id']})"

    @mcp.tool()
    async def get_event_details(event_id: int) -> str:
        """Get detailed information about a specific event."""
        data = await api.make_request("GET", f"{base_url}/api/events/{event_id}")
        
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

    @mcp.tool()
    async def update_event(
        event_id: int,
        title: str = None,
        content: str = None,
        start_date_time: str = None,
        organization_id: int = None,
        type_id: int = None,
        category_id: int = None,
        format_id: int = None,
        covers: list[str] = None,
        is_private: bool = None
    ) -> str:
        """Update an existing event."""
        payload = {}
        if title: payload["title"] = title
        if content: payload["content"] = content
        if start_date_time: payload["startDateTime"] = start_date_time
        if type_id: payload["typeId"] = type_id
        if category_id: payload["categoryId"] = category_id
        if format_id: payload["formatId"] = format_id
        if covers: payload["covers"] = covers
        if is_private is not None: payload["isPrivate"] = is_private

        data = await api.make_request(
            "PUT",
            f"{base_url}/api/events/organization/{organization_id}/{event_id}",
            json=payload
        )
        
        if not data or "data" not in data:
            return f"Failed to update event: {data.get('error', 'Unknown error')}"
        
        event = data["data"]
        return f"Event updated: {event['title']} (ID: {event['id']})"

    @mcp.tool()
    async def delete_event(event_id: int, organization_id: int) -> str:
        """Delete an event."""
        data = await api.make_request(
            "DELETE",
            f"{base_url}/api/events/organization/{organization_id}/{event_id}"
        )
        
        if not data or "data" not in data:
            return f"Failed to delete event: {data.get('error', 'Unknown error')}"
        
        return f"Event deleted (ID: {event_id})"

    # Organization Tools
    @mcp.tool()
    async def get_organizations() -> str:
        """List all organizations on yala.events."""
        data = await api.make_request("GET", f"{base_url}/api/organizations")
        
        if not data or "data" not in data:
            logger.warning("No organizations data received")
            return "Unable to fetch organizations or no organizations found."
        
        if not data["data"]:
            return "No organizations found."
        
        orgs = [f"Organization: {org['name']} | ID: {org['id']}" for org in data["data"]]
        return "\n---\n".join(orgs)

    @mcp.tool()
    async def create_organization(
        name: str,
        description: str = None,
        slug: str = None,
        logo: str = None,
        logo_miniature: str = None,
        cover_image: str = None
    ) -> str:
        """Create a new organization."""
        payload = {"name": name}
        if description: payload["description"] = description
        if slug: payload["slug"] = slug
        if logo: payload["logo"] = logo
        if logo_miniature: payload["logoMiniature"] = logo_miniature
        if cover_image: payload["coverImage"] = cover_image

        data = await api.make_request("POST", f"{base_url}/api/organizations", json=payload)
        
        if not data or "data" not in data:
            return f"Failed to create organization: {data.get('error', 'Unknown error')}"
        
        org = data["data"]
        return f"Organization created: {org['name']} (ID: {org['id']})"

    @mcp.tool()
    async def get_organization_details(organization_id: int) -> str:
        """Get detailed information about a specific organization."""
        data = await api.make_request("GET", f"{base_url}/api/organizations/{organization_id}")
        
        if not data or "data" not in data:
            return f"Unable to fetch organization details: {data.get('error', 'Organization not found')}"
        
        org = data["data"]
        details = [
            f"Name: {org['name']}",
            f"ID: {org['id']}",
            f"Slug: {org.get('slug', 'N/A')}",
            f"Description: {org.get('description', 'N/A')}",
            f"Logo: {org.get('logo', 'N/A')}",
            f"Logo Miniature: {org.get('logoMiniature', 'N/A')}",
            f"Cover Image: {org.get('coverImage', 'N/A')}"
        ]
        return "\n".join(details)

    @mcp.tool()
    async def update_organization(
        organization_id: int,
        name: str = None,
        description: str = None,
        slug: str = None,
        logo: str = None,
        logo_miniature: str = None,
        cover_image: str = None
    ) -> str:
        """Update an existing organization."""
        payload = {}
        if name: payload["name"] = name
        if description: payload["description"] = description
        if slug: payload["slug"] = slug
        if logo: payload["logo"] = logo
        if logo_miniature: payload["logoMiniature"] = logo_miniature
        if cover_image: payload["coverImage"] = cover_image

        data = await api.make_request(
            "PUT",
            f"{base_url}/api/organizations/{organization_id}",
            json=payload
        )
        
        if not data or "data" not in data:
            return f"Failed to update organization: {data.get('error', 'Unknown error')}"
        
        org = data["data"]
        return f"Organization updated: {org['name']} (ID: {org['id']})"

    @mcp.tool()
    async def delete_organization(organization_id: int) -> str:
        """Delete an organization."""
        data = await api.make_request("DELETE", f"{base_url}/api/organizations/{organization_id}")
        
        if not data or "data" not in data:
            return f"Failed to delete organization: {data.get('error', 'Unknown error')}"
        
        return f"Organization deleted (ID: {organization_id})"

    # User Tools
    @mcp.tool()
    async def list_users(search: str = None) -> str:
        """List users from yala.events."""
        params = {"search": search} if search else {}
        data = await api.make_request("GET", f"{base_url}/api/users", params=params)
        
        if not data or "data" not in data:
            return "Unable to fetch users or no users found."
        
        if not data["data"]:
            return "No users found."
        
        users = [f"User: {u['firstName']} {u['lastName']} | ID: {u['id']} | Email: {u.get('email', 'N/A')}" 
                 for u in data["data"]]
        return "\n---\n".join(users)

    @mcp.tool()
    async def create_user(
        first_name: str,
        last_name: str,
        email: str = None,
        phone: str = None,
        indicatif: str = None
    ) -> str:
        """Create a new user."""
        payload = {
            "firstName": first_name,
            "lastName": last_name
        }
        if email: payload["email"] = email
        if phone: payload["phone"] = phone
        if indicatif: payload["indicatif"] = indicatif

        data = await api.make_request("POST", f"{base_url}/api/users", json=payload)
        
        if not data or "data" not in data:
            return f"Failed to create user: {data.get('error', 'Unknown error')}"
        
        user = data["data"]
        return f"User created: {user['firstName']} {user['lastName']} (ID: {user['id']})"

    @mcp.tool()
    async def get_user_details(user_id: int) -> str:
        """Get detailed information about a specific user."""
        data = await api.make_request("GET", f"{base_url}/api/users/{user_id}")
        
        if not data or "data" not in data:
            return f"Unable to fetch user details: {data.get('error', 'User not found')}"
        
        user = data["data"]
        details = [
            f"Name: {user['firstName']} {user['lastName']}",
            f"ID: {user['id']}",
            f"Email: {user.get('email', 'N/A')}",
            f"Phone: {user.get('phone', 'N/A')}",
            f"Indicatif: {user.get('indicatif', 'N/A')}",
            f"Created At: {user['createdAt']}"
        ]
        return "\n".join(details)

    @mcp.tool()
    async def update_user(
        user_id: int,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        phone: str = None,
        indicatif: str = None
    ) -> str:
        """Update an existing user."""
        payload = {}
        if first_name: payload["firstName"] = first_name
        if last_name: payload["lastName"] = last_name
        if email: payload["email"] = email
        if phone: payload["phone"] = phone
        if indicatif: payload["indicatif"] = indicatif

        data = await api.make_request("PUT", f"{base_url}/api/users/{user_id}", json=payload)
        
        if not data or "data" not in data:
            return f"Failed to update user: {data.get('error', 'Unknown error')}"
        
        user = data["data"]
        return f"User updated: {user['firstName']} {user['lastName']} (ID: {user['id']})"

    @mcp.tool()
    async def delete_user(user_id: int) -> str:
        """Delete a user."""
        data = await api.make_request("DELETE", f"{base_url}/api/users/{user_id}")
        
        if not data or "data" not in data:
            return f"Failed to delete user: {data.get('error', 'Unknown error')}"
        
        return f"User deleted (ID: {user_id})"

    # Category Tools
    @mcp.tool()
    async def list_categories(search: str = None) -> str:
        """List event categories from yala.events."""
        params = {"search": search} if search else {}
        data = await api.make_request("GET", f"{base_url}/api/categories", params=params)
        
        if not data or "data" not in data:
            return "Unable to fetch categories or no categories found."
        
        if not data["data"]:
            return "No categories found."
        
        categories = [f"Category: {c['name']} | ID: {c['id']}" for c in data["data"]]
        return "\n---\n".join(categories)

    @mcp.tool()
    async def create_category(name: str) -> str:
        """Create a new event category."""
        payload = {"name": name}
        data = await api.make_request("POST", f"{base_url}/api/categories", json=payload)
        
        if not data or "data" not in data:
            return f"Failed to create category: {data.get('error', 'Unknown error')}"
        
        category = data["data"]
        return f"Category created: {category['name']} (ID: {category['id']})"

    @mcp.tool()
    async def get_category_details(category_id: int) -> str:
        """Get detailed information about a specific category."""
        data = await api.make_request("GET", f"{base_url}/api/categories/{category_id}")
        
        if not data or "data" not in data:
            return f"Unable to fetch category details: {data.get('error', 'Category not found')}"
        
        category = data["data"]
        details = [
            f"Name: {category['name']}",
            f"ID: {category['id']}",
            f"Created At: {category['createdAt']}"
        ]
        return "\n".join(details)

    @mcp.tool()
    async def update_category(category_id: int, name: str) -> str:
        """Update an existing category."""
        payload = {"name": name}
        data = await api.make_request("PUT", f"{base_url}/api/categories/{category_id}", json=payload)
        
        if not data or "data" not in data:
            return f"Failed to update category: {data.get('error', 'Unknown error')}"
        
        category = data["data"]
        return f"Category updated: {category['name']} (ID: {category['id']})"

    @mcp.tool()
    async def delete_category(category_id: int) -> str:
        """Delete a category."""
        data = await api.make_request("DELETE", f"{base_url}/api/categories/{category_id}")
        
        if not data or "data" not in data:
            return f"Failed to delete category: {data.get('error', 'Unknown error')}"
        
        return f"Category deleted (ID: {category_id})"

    # Tag Tools
    @mcp.tool()
    async def list_tags(search: str = None) -> str:
        """List tags from yala.events."""
        params = {"search": search} if search else {}
        data = await api.make_request("GET", f"{base_url}/api/tags", params=params)
        
        if not data or "data" not in data:
            return "Unable to fetch tags or no tags found."
        
        if not data["data"]:
            return "No tags found."
        
        tags = [f"Tag: {t['name']} | ID: {t['id']}" for t in data["data"]]
        return "\n---\n".join(tags)

    @mcp.tool()
    async def create_tag(name: str) -> str:
        """Create a new tag."""
        payload = {"name": name}
        data = await api.make_request("POST", f"{base_url}/api/tags", json=payload)
        
        if not data or "data" not in data:
            return f"Failed to create tag: {data.get('error', 'Unknown error')}"
        
        tag = data["data"]
        return f"Tag created: {tag['name']} (ID: {tag['id']})"

    @mcp.tool()
    async def get_tag_details(tag_id: int) -> str:
        """Get detailed information about a specific tag."""
        data = await api.make_request("GET", f"{base_url}/api/tags/{tag_id}")
        
        if not data or "data" not in data:
            return f"Unable to fetch tag details: {data.get('error', 'Tag not found')}"
        
        tag = data["data"]
        details = [
            f"Name: {tag['name']}",
            f"ID: {tag['id']}",
            f"Created At: {tag['createdAt']}"
        ]
        return "\n".join(details)

    @mcp.tool()
    async def update_tag(tag_id: int, name: str) -> str:
        """Update an existing tag."""
        payload = {"name": name}
        data = await api.make_request("PUT", f"{base_url}/api/tags/{tag_id}", json=payload)
        
        if not data or "data" not in data:
            return f"Failed to update tag: {data.get('error', 'Unknown error')}"
        
        tag = data["data"]
        return f"Tag updated: {tag['name']} (ID: {tag['id']})"

    @mcp.tool()
    async def delete_tag(tag_id: int) -> str:
        """Delete a tag."""
        data = await api.make_request("DELETE", f"{base_url}/api/tags/{tag_id}")
        
        if not data or "data" not in data:
            return f"Failed to delete tag: {data.get('error', 'Unknown error')}"
        
        return f"Tag deleted (ID: {tag_id})"

    # System Tools
    @mcp.tool()
    async def health_check() -> str:
        """Perform a health check on the application."""
        data = await api.make_request("GET", f"{base_url}/app/info/health-check")
        
        if not data:
            return "Health check failed."
        
        return "Application is healthy."

    return mcp

def main():
    """Run the MCP server."""
    logger.info("Starting Yala Events MCP server with stdio transport...")
    mcp = create_server()
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()