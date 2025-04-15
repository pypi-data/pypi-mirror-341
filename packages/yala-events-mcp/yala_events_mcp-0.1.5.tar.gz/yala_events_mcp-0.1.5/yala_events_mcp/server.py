import os
import sys
import logging
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from .api import YalaEventsAPI
from typing import Dict, List, Any, Optional

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
    async def fetch_events(
        search: Optional[str] = None,
        categories: Optional[str] = None,
        formats: Optional[str] = None,
        languages: Optional[str] = None,
        types: Optional[str] = None,
        ticket_types: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        current_page: Optional[int] = 1,
        per_page: Optional[int] = 10,
        tags: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fetch all events with optional filters."""
        params = {
            "search": search,
            "categories": categories,
            "formats": formats,
            "languages": languages,
            "types": types,
            "ticketTypes": ticket_types,
            "startDate": start_date,
            "endDate": end_date,
            "currentPage": str(current_page),
            "perPage": str(per_page),
            "tags": tags
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        try:
            data = await api.make_request("GET", f"{base_url}/api/events", params=params, headers={"Authorization": f"Bearer {api_token}"})
            if not data or "data" not in data:
                logger.warning("No events data received")
                return {"error": "Unable to fetch events"}
            return {
                "data": data["data"],
                "total": data.get("total", 0),
                "page": data.get("page", current_page),
                "perPage": data.get("perPage", per_page),
                "pages": data.get("pages", 1)
            }
        except Exception as e:
            logger.error(f"Error fetching events: {str(e)}")
            return {"error": "Failed to fetch events"}

    @mcp.tool()
    async def fetch_draft_events(
        current_page: Optional[int] = 1,
        per_page: Optional[int] = 10
    ) -> Dict[str, Any]:
        """Fetch draft events."""
        params = {"currentPage": str(current_page), "perPage": str(per_page)}
        try:
            data = await api.make_request("GET", f"{base_url}/api/events/draft", params=params, headers={"Authorization": f"Bearer {api_token}"})
            if not data or "data" not in data:
                logger.warning("No draft events data received")
                return {"error": "Unable to fetch draft events"}
            return {
                "data": data["data"],
                "total": data.get("total", 0),
                "page": data.get("page", current_page),
                "perPage": data.get("perPage", per_page),
                "pages": data.get("pages", 1)
            }
        except Exception as e:
            logger.error(f"Error fetching draft events: {str(e)}")
            return {"error": "Failed to fetch draft events"}

    @mcp.tool()
    async def fetch_published_events(
        current_page: Optional[int] = 1,
        per_page: Optional[int] = 10
    ) -> Dict[str, Any]:
        """Fetch published events."""
        params = {"currentPage": str(current_page), "perPage": str(per_page)}
        try:
            data = await api.make_request("GET", f"{base_url}/api/events/published", params=params, headers={"Authorization": f"Bearer {api_token}"})
            if not data or "data" not in data:
                logger.warning("No published events data received")
                return {"error": "Unable to fetch published events"}
            return {
                "data": data["data"],
                "total": data.get("total", 0),
                "page": data.get("page", current_page),
                "perPage": data.get("perPage", per_page),
                "pages": data.get("pages", 1)
            }
        except Exception as e:
            logger.error(f"Error fetching published events: {str(e)}")
            return {"error": "Failed to fetch published events"}

    @mcp.tool()
    async def fetch_public_events(
        search: Optional[str] = None,
        categories: Optional[str] = None,
        formats: Optional[str] = None,
        languages: Optional[str] = None,
        types: Optional[str] = None,
        ticket_types: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        current_page: Optional[int] = 1,
        per_page: Optional[int] = 10,
        tags: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fetch public events with filters."""
        params = {
            "search": search,
            "categories": categories,
            "formats": formats,
            "languages": languages,
            "types": types,
            "ticketTypes": ticket_types,
            "startDate": start_date,
            "endDate": end_date,
            "currentPage": str(current_page),
            "perPage": str(per_page),
            "tags": tags
        }
        params = {k: v for k, v in params.items() if v is not None}
        try:
            data = await api.make_request("GET", f"{base_url}/api/events/published", params=params)
            if not data or "data" not in data:
                logger.warning("No public events data received")
                return {"error": "Unable to fetch public events"}
            return {
                "data": data["data"],
                "total": data.get("total", 0),
                "page": data.get("page", current_page),
                "perPage": data.get("perPage", per_page),
                "pages": data.get("pages", 1)
            }
        except Exception as e:
            logger.error(f"Error fetching public events: {str(e)}")
            return {"error": "Failed to fetch public events"}

    @mcp.tool()
    async def fetch_event(event_slug: str) -> Dict[str, Any]:
        """Fetch an event by slug."""
        try:
            data = await api.make_request("GET", f"{base_url}/api/events/slug/{event_slug}", headers={"Authorization": f"Bearer {api_token}"})
            if not data or "data" not in data:
                logger.warning(f"Event not found for slug: {event_slug}")
                return {"error": "Event not found"}
            return data["data"]
        except Exception as e:
            logger.error(f"Error fetching event by slug: {str(e)}")
            return {"error": "Failed to fetch event"}

    @mcp.tool()
    async def fetch_public_event_by_slug(slug: str) -> Dict[str, Any]:
        """Fetch a public event by slug."""
        try:
            data = await api.make_request("GET", f"{base_url}/api/events/published/{slug}")
            if not data or "data" not in data:
                logger.warning(f"Public event not found for slug: {slug}")
                return {"error": "Public event not found"}
            return data["data"]
        except Exception as e:
            logger.error(f"Error fetching public event by slug: {str(e)}")
            return {"error": "Failed to fetch public event"}

    @mcp.tool()
    async def fetch_event_by_id(event_id: int) -> Dict[str, Any]:
        """Fetch an event by ID."""
        try:
            data = await api.make_request("GET", f"{base_url}/api/events/{event_id}")
            if not data or "data" not in data:
                logger.warning(f"Event not found for ID: {event_id}")
                return {"error": "Event not found"}
            return data["data"]
        except Exception as e:
            logger.error(f"Error fetching event by ID: {str(e)}")
            return {"error": "Failed to fetch event"}

    @mcp.tool()
    async def fetch_event_tickets(organization_id: int, event_id: int) -> List[Dict[str, Any]]:
        """Fetch tickets for an event."""
        try:
            data = await api.make_request("GET", f"{base_url}/api/events-tickets/{organization_id}/{event_id}")
            if not data or "data" not in data:
                logger.warning(f"No tickets found for event ID: {event_id}")
                return []
            return data["data"]
        except Exception as e:
            logger.error(f"Error fetching tickets: {str(e)}")
            return []

    @mcp.tool()
    async def fetch_organization_events(organization_id: int, current_page: Optional[int] = 1, per_page: Optional[int] = 10) -> Dict[str, Any]:
        """Fetch events for an organization."""
        params = {"currentPage": str(current_page), "perPage": str(per_page)}
        try:
            data = await api.make_request("GET", f"{base_url}/api/events/organization/{organization_id}", params=params, headers={"Authorization": f"Bearer {api_token}"})
            if not data or "data" not in data:
                logger.warning(f"No events found for organization ID: {organization_id}")
                return {"error": "No events found"}
            return {
                "data": data["data"],
                "total": data.get("total", 0),
                "page": data.get("page", current_page),
                "perPage": data.get("perPage", per_page),
                "pages": data.get("pages", 1)
            }
        except Exception as e:
            logger.error(f"Error fetching organization events: {str(e)}")
            return {"error": "Failed to fetch organization events"}

    @mcp.tool()
    async def fetch_published_organization_events(organization_id: int, current_page: Optional[int] = 1, per_page: Optional[int] = 10) -> Dict[str, Any]:
        """Fetch published events for an organization."""
        params = {"currentPage": str(current_page), "perPage": str(per_page)}
        try:
            data = await api.make_request("GET", f"{base_url}/api/events/published/organization/{organization_id}", params=params)
            if not data or "data" not in data:
                logger.warning(f"No published events found for organization ID: {organization_id}")
                return {"error": "No published events found"}
            return {
                "data": data["data"],
                "total": data.get("total", 0),
                "page": data.get("page", current_page),
                "perPage": data.get("perPage", per_page),
                "pages": data.get("pages", 1)
            }
        except Exception as e:
            logger.error(f"Error fetching published organization events: {str(e)}")
            return {"error": "Failed to fetch published organization events"}

    @mcp.tool()
    async def create_event(
        organization_id: int,
        title: str,
        content: str,
        start_date_time: str,
        type_id: int,
        category_id: int,
        format_id: int,
        covers: List[str],
        is_private: bool
    ) -> Dict[str, Any]:
        """Create a new event."""
        payload = {
            "title": title,
            "content": content,
            "startDateTime": start_date_time,
            "typeId": type_id,
            "categoryId": category_id,
            "formatId": format_id,
            "covers": covers,
            "isPrivate": is_private
        }
        try:
            data = await api.make_request(
                "POST",
                f"{base_url}/api/events/organization/{organization_id}",
                json=payload,
                headers={"Authorization": f"Bearer {api_token}"}
            )
            if not data or "data" not in data:
                logger.warning(f"Failed to create event: {data.get('error', 'Unknown error')}")
                return {"error": "Failed to create event"}
            logger.info(f"Created event: {data['data']['title']} (ID: {data['data']['id']})")
            return data["data"]
        except Exception as e:
            logger.error(f"Error creating event: VECTOR_SIZE_EXCEEDED")
            return {"error": "Failed to create event"}

    @mcp.tool()
    async def update_event(
        organization_id: int,
        event_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        start_date_time: Optional[str] = None,
        type_id: Optional[int] = None,
        category_id: Optional[int] = None,
        format_id: Optional[int] = None,
        covers: Optional[List[str]] = None,
        is_private: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Update an existing event."""
        payload = {}
        if title is not None:
            payload["title"] = title
        if content is not None:
            payload["content"] = content
        if start_date_time is not None:
            payload["startDateTime"] = start_date_time
        if type_id is not None:
            payload["typeId"] = type_id
        if category_id is not None:
            payload["categoryId"] = category_id
        if format_id is not None:
            payload["formatId"] = format_id
        if covers is not None:
            payload["covers"] = covers
        if is_private is not None:
            payload["isPrivate"] = is_private
        try:
            data = await api.make_request(
                "PUT",
                f"{base_url}/api/events/organization/{organization_id}/{event_id}",
                json=payload,
                headers={"Authorization": f"Bearer {api_token}"}
            )
            if not data or "data" not in data:
                logger.warning(f"Failed to update event: {data.get('error', 'Unknown error')}")
                return {"error": "Failed to update event"}
            logger.info(f"Updated event: {data['data']['title']} (ID: {event_id})")
            return data["data"]
        except Exception as e:
            logger.error(f"Error updating event: {str(e)}")
            return {"error": "Failed to update event"}

    @mcp.tool()
    async def update_event_media(organization_id: int, event_id: int, media_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update event media."""
        try:
            data = await api.make_request(
                "PUT",
                f"{base_url}/api/events/organization/media/{organization_id}/{event_id}",
                data=media_data,
                headers={"Authorization": f"Bearer {api_token}", "Content-Type": "multipart/form-data"}
            )
            if not data or "data" not in data:
                logger.warning(f"Failed to update event media: {data.get('error', 'Unknown error')}")
                return {"error": "Failed to update event media"}
            return data["data"]
        except Exception as e:
            logger.error(f"Error updating event media: {str(e)}")
            return {"error": "Failed to update event media"}

    @mcp.tool()
    async def delete_event(organization_id: int, event_id: int) -> Dict[str, Any]:
        """Delete an event."""
        try:
            data = await api.make_request(
                "DELETE",
                f"{base_url}/api/events/organization/{organization_id}/{event_id}",
                headers={"Authorization": f"Bearer {api_token}"}
            )
            if not data:
                logger.warning(f"Failed to delete event: {data.get('error', 'Unknown error')}")
                return {"error": "Failed to delete event"}
            logger.info(f"Deleted event ID: {event_id}")
            return {}
        except Exception as e:
            logger.error(f"Error deleting event: {str(e)}")
            return {"error": "Failed to delete event"}

    @mcp.tool()
    async def update_event_publish_status(organization_id: int, event_id: int, draft: bool) -> Dict[str, Any]:
        """Update event publish status."""
        payload = {"draft": draft}
        try:
            data = await api.make_request(
                "PUT",
                f"{base_url}/api/events/organization/publish/{organization_id}/{event_id}",
                json=payload,
                headers={"Authorization": f"Bearer {api_token}"}
            )
            if not data or "data" not in data:
                logger.warning(f"Failed to update publish status: {data.get('error', 'Unknown error')}")
                return {"error": "Failed to update publish status"}
            return data["data"]
        except Exception as e:
            logger.error(f"Error updating publish status: {str(e)}")
            return {"error": "Failed to update publish status"}

    return mcp

def main():
    """Run the MCP server."""
    logger.info("Starting Yala Events MCP server with stdio transport...")
    mcp = create_server()
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()