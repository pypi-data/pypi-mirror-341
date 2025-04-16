"""Update employees tool."""

from typing import List, Optional, Union
from datetime import date

from pydantic import BaseModel

from tools.base import BaseTool
from tools.result import ToolResult


class Address(BaseModel):
    """Address model."""
    additional_address_line: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    postal_code: Optional[str] = None
    country_code_iso2: Optional[str] = None


class UpdateEmployeeInput(BaseModel):
    """Input for UpdateEmployeeTool."""

    employee_id: Optional[Union[str, int]] = None
    role: Optional[str] = None
    given_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    foreign_id: Optional[str] = None
    employment_start_date: Optional[date] = None
    employment_end_date: Optional[date] = None
    personal_email: Optional[str] = None
    personal_phone_number: Optional[str] = None
    address: Optional[Address] = None


class UpdateEmployeeTool(BaseTool):
    """Tool for updating employees."""

    @staticmethod
    def name() -> str:
        """The name of the tool."""
        return "update_employee"

    @staticmethod
    def description() -> str:
        """The description of the tool."""
        return """
Updates an employee with the given data. Make sure to ask the user for all this information, none of them are required:

- role: the role of the employee (name of the department)
- given_name: the first name of the employee
- last_name: the last name of the employee
- email: the email of the employee
- phone_number: the phone number of the employee
- foreign_id: the foreign id of the employee
- employment_start_date: the start date of the employee's employment
- employment_end_date: the end date of the employee's employment
- personal_email: the personal email of the employee
- personal_phone_number: the personal phone number of the employee
- address: the address of the employee, formed by the following fields:
  - address_line_1: the first line of the address
  - address_line_2: the second line of the address
  - additional_address_line: the additional address line
  - city: the city of the address
  - region: the region of the address
  - postal_code: the postal code of the address
  - country_code_iso2: the country code iso2 of the address

You should always confirm with the user that the information is correct before calling this tool.
"""

    async def execute(self, input_data: UpdateEmployeeInput) -> ToolResult:
        """Execute the tool."""
        employee_id = input_data.employee_id
        del input_data.employee_id

        response = self.client.patch(f"/employees/{employee_id}", data=input_data.model_dump())
        return ToolResult(
            data=response,
            error=None
        )
