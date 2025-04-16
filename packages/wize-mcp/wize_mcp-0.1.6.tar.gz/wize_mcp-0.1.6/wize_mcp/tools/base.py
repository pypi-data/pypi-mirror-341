"""Base tools for the Workwize MCP server."""
from abc import ABC, abstractmethod
from .result import ToolResult
from wize_mcp.api.client import WorkwizeClient

class BaseTool(ABC):
    """Base tool for the Workwize MCP server."""
    def __init__(self):
        self.client = WorkwizeClient()

    @staticmethod
    def name() -> str:
        """The name of the tool."""
        pass

    @staticmethod
    def description() -> str:
        """The description of the tool."""
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """Execute the tool."""
        pass
