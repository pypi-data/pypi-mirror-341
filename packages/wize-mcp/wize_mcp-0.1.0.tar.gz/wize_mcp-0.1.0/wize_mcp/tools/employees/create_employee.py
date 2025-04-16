"""Create employee tool."""

from typing import Optional
from datetime import date

from pydantic import BaseModel

from tools.base import BaseTool
from tools.result import ToolResult


class CreateEmployeeInput(BaseModel):
    """Input for CreateEmployeeTool."""

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


class CreateEmployeeTool(BaseTool):
    """Tool for creating employees."""

    @staticmethod
    def name() -> str:
        """The name of the tool."""
        return "create_employee"

    @staticmethod
    def description() -> str:
        """The description of the tool."""
        return """
Creates an employee with the given data. Make sure to ask the user for all this information:

- role: the role of the employee (name of the department)
- given_name: the first name of the employee
- last_name: the last name of the employee
- email: the email of the employee
- phone_number: the phone number of the employee
- is_notified: whether the employee should be notified
- employment_start_date: the start date of the employee's employment
- employment_end_date: the end date of the employee's employment
- personal_email: the personal email of the employee
- personal_phone_number: the personal phone number of the employee

You should always confirm with the user that the information is correct before calling this tool.
"""
    async def execute(self, input_data: CreateEmployeeInput) -> ToolResult:
        """Execute the tool."""
        response = self.client.post("/employees", data=input_data.model_dump())
        return ToolResult(
            data=response,
            error=None
        )
