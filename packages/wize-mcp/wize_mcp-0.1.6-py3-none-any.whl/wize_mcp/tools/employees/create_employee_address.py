"""Create employees address tool."""

from typing import Optional

from pydantic import BaseModel, Field

from wize_mcp.tools.base import BaseTool
from wize_mcp.tools.result import ToolResult


class CreateEmployeeAddressInput(BaseModel):
    """Address model."""

    employee_id: int
    company_name: Optional[str] = None
    address_line_1: str = Field(..., max_length=255)
    address_line_2: Optional[str] = None
    additional_address_line: Optional[str] = Field(None, max_length=255)
    city: str = Field(..., max_length=255)
    region: Optional[str] = None
    postal_code: str = Field(..., max_length=20)
    country_id: int
    phone_number: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    last_name: Optional[str] = None
    postcode: Optional[str] = None


class CreateEmployeeAddressTool(BaseTool):
    """Tool for creating employees address."""

    @staticmethod
    def name() -> str:
        """The name of the tool."""
        return "create_employee_address"

    @staticmethod
    def description() -> str:
        """The description of the tool."""
        return """
Creates an employee address with the given data. Make sure to ask for the following information from the user before calling this tool:

- company_name: the name of the company
- address_line_1: the first line of the address
- address_line_2: the second line of the address
- additional_address_line: the additional address line
- city: the city of the address
- region: the region of the address
- postal_code: the postal code of the address
- country_id: the id of the country
- phone_number: the phone number of the owner of the address
- email: the email of the owner of the address
- name: the name of the owner of the address
- last_name: the last name of the owner of the address

You should always confirm with the user that the information is correct before calling this tool.
"""

    async def execute(self, input_data: CreateEmployeeAddressInput) -> ToolResult:
        """Execute the tool."""
        employee_id = input_data.employee_id
        del input_data.employee_id

        data = input_data.model_dump()
        data['postcode'] = data['postal_code']

        response = self.client.post(f"/employees/{employee_id}/addresses", data=data)
        return ToolResult(
            data=response,
            error=None
        )
