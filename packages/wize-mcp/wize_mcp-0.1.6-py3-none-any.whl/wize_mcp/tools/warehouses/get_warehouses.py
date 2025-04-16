"""Get warehouses tool."""

from wize_mcp.tools.base import BaseTool
from wize_mcp.tools.result import ToolResult

class GetWarehousesTool(BaseTool):
    """Tool for getting warehouses."""

    @staticmethod
    def name() -> str:
        """The name of the tool."""
        return "get_warehouses"

    @staticmethod
    def description() -> str:
        """The description of the tool."""
        return "Get a list of all available warehouses"

    async def execute(self, input_data = None) -> ToolResult:
        """Execute the tool."""
        response = self.client.get("/warehouses")
        return ToolResult(
            data=response,
            error=None
        )
