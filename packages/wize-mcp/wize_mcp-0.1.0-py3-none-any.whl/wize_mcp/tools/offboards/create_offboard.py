"""Create offboard tool."""

from typing import Optional, List, Union
from enum import Enum

from pydantic import BaseModel

from tools.base import BaseTool
from tools.result import ToolResult

class PossibleStatuses(str, Enum):
    """Possible statuses for the offboard."""
    SCHEDULED = 'scheduled'
    REQUEST_RECEIVED = 'request_received'

class PossibleDestinationTypes(str, Enum):
    """Possible destination types for the offboard."""
    WAREHOUSE = 'warehouse'
    OFFICE = 'office'

class CreateOffboardInput(BaseModel):
    """Input for CreateOffboardTool."""

    employee_id: int
    assets: List[int]
    destination_type: PossibleDestinationTypes
    destination_code: Union[int, str]
    status: Optional[PossibleStatuses]


class CreateOffboardTool(BaseTool):
    """Tool for creating offboards."""

    @staticmethod
    def name() -> str:
        """The name of the tool."""
        return "create_offboard"

    @staticmethod
    def description() -> str:
        """The description of the tool."""
        return """
Creates an offboard for the provided employee with the given data. To create it properly, you need the employee ID (which you can get with the `get_employees` tool), a list of asset ids, a destination type (warehouse or office) and a destination id (which you can get with the `get_warehouses` or `get_offices` tool).

You can also provide a status, which can be:
- scheduled: the offboard is scheduled
- request_received: the offboard request has been received

You should always confirm with the user that the information is correct before calling this tool.
"""

    async def execute(self, input_data: CreateOffboardInput) -> ToolResult:
        """Execute the tool."""
        response = self.client.post("/requests/offboards", data=input_data.model_dump())
        return ToolResult(
            data=response,
            error=None
        )
