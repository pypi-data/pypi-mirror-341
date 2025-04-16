"""Get orders tool."""

from typing import List, Optional
from datetime import date

from pydantic import BaseModel

from wize_mcp.tools.base import BaseTool
from wize_mcp.tools.result import ToolResult


class GetOrdersInput(BaseModel):
    """Input for GetOrdersTool."""

    page: Optional[int] = 1
    per_page: Optional[int] = 20
    employee_foreign_id: Optional[str] = None
    number: Optional[str] = None


class GetOrdersTool(BaseTool):
    """Tool for getting orders."""

    @staticmethod
    def name() -> str:
        """The name of the tool."""
        return "get_orders"

    @staticmethod
    def description() -> str:
        """The description of the tool."""
        return """
Get a list of orders with filtering options.

You can filter by:
- employee_foreign_id: the foreign id of the employee (from an HRIS system)
- number: the number of the order. You can use this parameter to search for a specific order
"""

    async def execute(self, input_data: GetOrdersInput) -> ToolResult:
        """Execute the tool."""
        params = {
            "page": input_data.page,
            "per_page": input_data.per_page,
        }
        for key, value in input_data.model_dump().items():
            if key in ['per_page', 'page']:
                continue
            params[f"filter[{key}]"] = value

        response = self.client.get("/orders", params=params)
        return ToolResult(
            data=response,
            error=None
        )
