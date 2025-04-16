"""Workwize API client module."""
from typing import Any, Dict, Optional

import httpx

from wize_mcp.config import config

class WorkwizeAPIError(Exception):
    """Custom exception for Workwize API errors."""
    pass

class WorkwizeClient:
    """Client for interacting with the Workwize Public API."""

    def __init__(self, api_token: Optional[str] = None):
        """Initialize the client.

        Args:
            api_token: Optional API token. If not provided, uses the one from config.
        """
        self.api_token = api_token or config.api_token
        self.base_url = config.api_base_url
        self.client = httpx.Client(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_token}",
                "Accept": "application/json",
                "X-Client-Id": "Workwize-MCP-Client",
            },
            timeout=30.0
        )

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle API response and errors.

        Args:
            response: The API response to handle.

        Returns:
            The JSON response data.

        Raises:
            WorkwizeAPIError: If the API returns an error.
        """
        try:
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_data = e.response.json() if e.response.content else {}
            raise WorkwizeAPIError(
                f"API request failed: {e.response.status_code} - {error_data}"
            ) from e
        except Exception as e:
            raise WorkwizeAPIError(f"Unexpected error: {str(e)}") from e

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = self.client.get(path, params=params)
        return self._handle_response(response)

    def post(self, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = self.client.post(path, json=data)
        return self._handle_response(response)

    def put(self, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = self.client.put(path, json=data)
        return self._handle_response(response)

    def patch(self, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = self.client.patch(path, json=data)
        return self._handle_response(response)

    def delete(self, path: str) -> Dict[str, Any]:
        response = self.client.delete(path)
        return self._handle_response(response)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.client.close()
