"""Workwize API client module."""
from typing import Any, Dict, Optional
from datetime import date

import httpx
from pydantic import BaseModel

from config import config

class WorkwizeAPIError(Exception):
    """Custom exception for Workwize API errors."""
    pass

class OrderFilter(BaseModel):
    """Model for order filter parameters."""
    employee_foreign_id: Optional[str] = None
    number: Optional[str] = None
    per_page: Optional[int] = None

class AssetFilter(BaseModel):
    """Model for asset filter parameters."""
    employee_id: Optional[str] = None
    employee_email: Optional[str] = None
    country_availability: Optional[str] = None
    per_page: Optional[int] = 200
    page: Optional[int] = None

class CreateAssetData(BaseModel):
    """Model for creating an asset."""
    name: str
    type: str  # "Buy" or "Rent"
    category_id: int
    budget_deduction: float
    date_ordered: date
    currency: str
    depreciation_months: Optional[int] = None
    invoice_price: Optional[float] = None
    rent_end_date: Optional[date] = None
    note: Optional[str] = None
    tags: Optional[list[int]] = None
    serial_code: Optional[str] = None
    image: Optional[list[str]] = None
    warehouse_status: Optional[str] = None

class CreateAddressData(BaseModel):
    """Model for creating an address."""
    city: str
    postal_code: str
    country_id: int
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    additional_address_line: Optional[str] = None
    region: Optional[str] = None
    phone_number: Optional[str] = None

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
