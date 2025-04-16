"""Get offboards tool."""

from typing import Optional
from enum import Enum

from pydantic import BaseModel

from tools.base import BaseTool
from tools.result import ToolResult

class PossibleStatuses(str, Enum):
    """Possible statuses for the offboard."""
    REQUEST_RECEIVED = 'request_received'
    REQUEST_BEING_PROCESSED = 'request_being_processed'
    PENDING_EMPLOYEE_RESPONSE = 'pending_employee_response'
    PENDING_PICK_UP_DATE_CHOOSEN = 'pending_pick_up_date_choosen'
    PICK_UP_IN_PROGRESS = 'pick_up_in_progress'
    PICK_UP_DROP_OFF_IN_PROGRESS = 'pick_up_drop_off_in_progress'
    PICK_UP_FAILED = 'pick_up_failed'
    OFFBOARD_CANCELLED = 'offboard_cancelled'
    OFFBOARD_COMPLETED = 'offboard_completed'
    OFFBOARD_FAILED_PICKUP_FAILED = 'offboard_failed_pickup_failed'
    OFFBOARD_FAILED_NO_ANSWER = 'offboard_failed_no_answer'
    POSTPONED_BY_USER = 'postponed_by_user'
    PENDING_EMPLOYEE_RESPONSE1 = 'pending_employee_response1'
    PENDING_EMPLOYEE_RESPONSE2 = 'pending_employee_response2'
    PENDING_EMPLOYEE_RESPONSE3 = 'pending_employee_response3'
    PENDING_EMPLOYEE_RESPONSE4 = 'pending_employee_response4'
    DETAILS_CONFIRMED = 'details_confirmed'
    IN_TRANSIT_TO_WAREHOUSE = 'in_transit_to_warehouse'
    MANUAL_SNIPPET_SENT = 'manual_snippet_sent'
    MANUAL_SNIPPET_SENT2 = 'manual_snippet_sent2'
    SCHEDULED = 'scheduled'
    BEING_STOCKED_AT_WAREHOUSE = 'being_stocked_at_warehouse'

class GetOffboardsInput(BaseModel):
    """Input for GetOffboardsTool."""

    per_page: Optional[int] = 25
    page: Optional[int] = 1
    search: Optional[str] = None
    status: Optional[PossibleStatuses] = None
    employee_id: Optional[int] = None
    employee_foreign_id: Optional[str] = None

class GetOffboardsTool(BaseTool):
    """Tool for getting offboards."""

    @staticmethod
    def name() -> str:
        """The name of the tool."""
        return "get_offboards"

    @staticmethod
    def description() -> str:
        """The description of the tool."""
        return """
Get a list of offboards with filtering options.

You can filter by:
- status: the status of the offboard
- employee_id: the id of the employee
- employee_foreign_id: the foreign id of the employee
- search: a search query to search for a specific offboard (for example, the name or email of the employee)
"""
    async def execute(self, input_data: GetOffboardsInput) -> ToolResult:
        """Execute the tool."""
        input_params = input_data.model_dump(exclude_none=True)
        params = {
            "per_page": input_data.per_page,
            "page": input_data.page,
        }
        for key, value in input_params.items():
            if key in ['per_page', 'page']:
                continue
            params[f"filter[{key}]"] = value

        response = self.client.get("/offboards", params=params)
        return ToolResult(
            data=response,
            error=None
        )
