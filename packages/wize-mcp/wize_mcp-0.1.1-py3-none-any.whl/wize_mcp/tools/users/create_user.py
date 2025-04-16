"""Create user tool."""

from typing import Optional
from datetime import date

from pydantic import BaseModel

from wize_mcp.tools.base import BaseTool
from wize_mcp.tools.result import ToolResult


class Address(BaseModel):
    """Address model for user."""

    address_line_1: str
    city: str
    region: str
    postal_code: str
    country_code_iso2: str
    address_line_2: Optional[str] = None
    additional_address_line: Optional[str] = None


class CreateUserInput(BaseModel):
    """Input for CreateUserTool."""

    role: str
    given_name: str
    last_name: str
    email: str
    phone_number: str
    is_notified: bool = False
    employment_start_date: Optional[date] = None
    employment_end_date: Optional[date] = None
    personal_email: Optional[str] = None
    personal_phone_number: Optional[str] = None
    foreign_id: Optional[str] = None
    address: Optional[Address] = None


class CreateUserTool(BaseTool):
    """Tool for creating users."""

    @staticmethod
    def name() -> str:
        """The name of the tool."""
        return "create_user"

    @staticmethod
    def description() -> str:
        """The description of the tool."""
        return """
Creates an user with the given data. Before calling this tool, make sure to retrieve the following information:
- role: a department name
- given_name: the first name of the user
- last_name: the last name of the user
- email: the email of the user
- phone_number: the phone number of the user
- is_notified: whether the user should be notified
- employment_start_date: the start date of the user's employment
- employment_end_date: the end date of the user's employment
- personal_email: the personal email of the user
- personal_phone_number: the personal phone number of the user
- foreign_id: the foreign id of the user (from an HRIS system)
- address: the address of the user, formed by the following fields:
  - address_line_1: the first line of the address
  - address_line_2: the second line of the address
  - city: the city of the address
  - region: the region of the address
  - postal_code: the postal code of the address
  - country_code_iso2: the country code iso2 of the address

You should always confirm with the user that the information is correct before calling this tool.
"""

    async def execute(self, input_data: CreateUserInput) -> ToolResult:
        """Execute the tool."""
        response = self.client.post("/users", data=input_data.model_dump())
        return ToolResult(
            data=response,
            error=None
        )
