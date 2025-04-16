"""Get offices tool."""

from typing import Optional

from pydantic import BaseModel

from tools.base import BaseTool
from tools.result import ToolResult

class GetOfficesInput(BaseModel):
    """Input for GetOfficesTool."""

    page: Optional[int] = 1
    name: Optional[str] = None

class GetOfficesTool(BaseTool):
    """Tool for getting offices."""

    @staticmethod
    def name() -> str:
        """The name of the tool."""
        return "get_offices"

    @staticmethod
    def description() -> str:
        """The description of the tool."""
        return """
Get a list of all available offices.

You can filter by:
- name: the name of the office
"""

    async def execute(self, input_data: GetOfficesInput) -> ToolResult:
        """Execute the tool."""
        params = {
            "page": input_data.page,
        }
        for key, value in input_data.model_dump().items():
            if key in ['page']:
                continue
            params[f"filter[{key}]"] = value

        response = self.client.get("/offices", params=params)
        return ToolResult(
            data=response,
            error=None
        )
