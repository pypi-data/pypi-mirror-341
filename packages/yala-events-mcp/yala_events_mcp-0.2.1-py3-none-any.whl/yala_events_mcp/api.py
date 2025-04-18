import os
import httpx
import logging
from typing import Any

logger = logging.getLogger(__name__)

class YalaEventsAPI:
    def __init__(self, api_token: str, base_url: str):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    async def make_request(
        self, 
        method: str, 
        url: str, 
        json: dict = None, 
        params: dict = None
    ) -> dict[str, Any] | None:
        """Make a request to the yala.events API with error handling."""
        async with httpx.AsyncClient() as client:
            try:
                logger.info(f"Making {method} request to {url}")
                response = await client.request(
                    method=method,
                    url=url,
                    headers=self.headers,
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
