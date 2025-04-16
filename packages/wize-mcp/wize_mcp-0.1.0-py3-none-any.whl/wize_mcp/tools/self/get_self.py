"""Get self tool."""

from tools.base import BaseTool
from tools.result import ToolResult

class GetSelfTool(BaseTool):
    """Tool for getting self information."""

    @staticmethod
    def name() -> str:
        """The name of the tool."""
        return "get_self"

    @staticmethod
    def description() -> str:
        """The description of the tool."""
        return "Get information about the authenticated user"

    async def execute(self) -> ToolResult:
        response = self.client.get("/self")
        return ToolResult(
            data=response,
            error=None
        )
