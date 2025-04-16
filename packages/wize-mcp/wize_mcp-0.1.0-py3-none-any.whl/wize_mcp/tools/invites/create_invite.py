"""Create invite tool."""

from typing import Optional
from datetime import date

from pydantic import BaseModel

from tools.base import BaseTool
from tools.result import ToolResult


class CreateInviteInput(BaseModel):
    """Input for CreateInviteTool."""

    email: str


class CreateInviteTool(BaseTool):
    """Tool for creating invites."""

    @staticmethod
    def name() -> str:
        """The name of the tool."""
        return "create_invite"

    @staticmethod
    def description() -> str:
        """The description of the tool."""
        return """
Creates an invite with the given data. Make sure to ask the user for all this information:

- email: the email of the invite

You should always confirm with the user that the information is correct before calling this tool.
"""

    async def execute(self, input_data: CreateInviteInput) -> ToolResult:
        """Execute the tool."""
        response = self.client.post("/invites", data=input_data.model_dump())
        return ToolResult(
            data=response,
            error=None
        )
