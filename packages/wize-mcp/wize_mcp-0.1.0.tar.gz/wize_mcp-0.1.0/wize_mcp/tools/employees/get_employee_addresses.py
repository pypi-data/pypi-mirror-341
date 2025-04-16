"""Get employees addresses tool."""

from typing import Union

from pydantic import BaseModel

from tools.base import BaseTool
from tools.result import ToolResult


class GetEmployeeAddressesInput(BaseModel):
    """Input for GetEmployeeAddressesTool."""

    employee_id: Union[int, str]


class GetEmployeeAddressesTool(BaseTool):
    """Tool for getting employee addresses."""

    @staticmethod
    def name() -> str:
        """The name of the tool."""
        return "get_employee_addresses"

    @staticmethod
    def description() -> str:
        """The description of the tool."""
        return "Get the addresses associated with the employee. You need an employee id to call this tool. You can get it by calling the get_employees tool and filtering by email, so make sure to ask for it if the user doesn't provide it."

    async def execute(self, input_data: GetEmployeeAddressesInput) -> ToolResult:
        """Execute the tool."""
        response = self.client.get(f"/employees/{input_data.employee_id}/addresses")
        return ToolResult(
            data=response,
            error=None
        )
