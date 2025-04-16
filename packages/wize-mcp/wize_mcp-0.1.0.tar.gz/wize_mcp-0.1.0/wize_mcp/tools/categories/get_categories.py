"""Get categories tool."""

from tools.base import BaseTool
from tools.result import ToolResult

class GetCategoriesTool(BaseTool):
    """Tool for getting categories."""

    @staticmethod
    def name() -> str:
        """The name of the tool."""
        return "get_categories"

    @staticmethod
    def description() -> str:
        """The description of the tool."""
        return "Get a list of all available product categories"

    async def execute(self, input_data = None) -> ToolResult:
        """Execute the tool."""
        response = self.client.get("/categories")
        return ToolResult(
            data=response,
            error=None
        )
