"""Get assets tool."""

from typing import List, Optional

from pydantic import BaseModel

from wize_mcp.tools.base import BaseTool
from wize_mcp.tools.result import ToolResult


class GetAssetsInput(BaseModel):
    """Input for GetAssetsTool."""

    per_page: Optional[int] = 25
    page: Optional[int] = 1
    id: Optional[int] = None
    serial_code: Optional[str] = None
    categories: Optional[List[int]] = None
    employeeId: Optional[int] = None
    employeeEmail: Optional[str] = None
    external_reference: Optional[str] = None
    search: Optional[str] = None

class GetAssetsTool(BaseTool):
    """Tool for getting assets."""

    @staticmethod
    def name() -> str:
        """The name of the tool."""
        return "get_assets"

    @staticmethod
    def description() -> str:
        """The description of the tool."""
        return """
Get a list of assets with filtering options.

You can filter by:
- id: the id of the asset
- serial_code: the serial code of the asset
- categories: a list of category ids
- employeeId: the id of the employee who owns the asset
- employeeEmail: the email of the employee who owns the asset
- external_reference: the external reference of the asset
- search: a search query to search for a specific asset (for example, the name)
"""
    async def execute(self, input_data: GetAssetsInput) -> ToolResult:
        """Execute the tool."""
        input_params = input_data.model_dump(exclude_none=True)
        params = {
            "per_page": input_data.per_page,
            "page": input_data.page,
        }
        for key, value in input_params.items():
            if key in ['id', 'per_page', 'page']:
                continue
            params[f"filter[{key}]"] = value

        response = self.client.get("/assets", params=params)
        return ToolResult(
            data=response,
            error=None
        )
