"""Create employees asset tool."""

from datetime import date
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field, field_validator, model_validator

from wize_mcp.tools.base import BaseTool
from wize_mcp.tools.result import ToolResult


class InventoryStatusEnum(str, Enum):
    """Inventory status enum."""
    AVAILABLE = 'available'
    UNAVAILABLE = 'unavailable'
    UNKNOWN = 'unknown'
    IN_REPAIR = 'in_repair'


class CreateEmployeeAssetInput(BaseModel):
    """Asset model."""

    employee_id: int
    name: str
    type: str
    category_id: int
    depreciation_months: Optional[int] = None
    budget_deduction: Union[float, int]
    invoice_price: Optional[Union[float, int]] = None
    date_ordered: date
    currency: str
    rent_end_date: Optional[date] = None
    note: Optional[str] = None
    tags: Optional[List[str]] = None
    serial_code: Optional[str] = None
    image: Optional[str] = None
    warehouse_status: InventoryStatusEnum = InventoryStatusEnum.UNKNOWN

    @model_validator(mode='after')
    def validate_depreciation_months(self) -> 'CreateEmployeeAssetInput':
        """Validate depreciation_months based on type."""
        if self.type == 'Buy' and (self.depreciation_months is None or self.depreciation_months < 1):
            raise ValueError('depreciation_months should be at least 1 month for Buy type')
        if self.type == 'Rent' and self.depreciation_months is not None:
            raise ValueError('depreciation_months should not be included for Rent type')
        return self


class CreateEmployeeAssetTool(BaseTool):
    """Tool for creating employees asset."""

    @staticmethod
    def name() -> str:
        """The name of the tool."""
        return "create_employee_asset"

    @staticmethod
    def description() -> str:
        """The description of the tool."""
        return """
Creates an asset owned by the provided employee with the given data. Make sure to ask the user for all this information:

- name: the name of the asset
- type: the type of the asset (Buy or Rent)
- category_id: the id of the category of the asset
- depreciation_months: the number of months the asset will be depreciated
- budget_deduction: the amount of the budget deduction for the asset
- invoice_price: the price of the asset
- date_ordered: the date the asset was ordered
- currency: the currency of the asset
- rent_end_date: the date the asset will be returned
- note: a note for the asset
- tags: a list of tags for the asset
- serial_code: the serial code of the asset
- image: the image of the asset
- warehouse_status: the status of the asset in the warehouse (available, unavailable, unknown, in repair)

You should always confirm with the user that the information is correct before calling this tool.
"""

    async def execute(self, input_data: CreateEmployeeAssetInput) -> ToolResult:
        """Execute the tool."""
        employee_id = input_data.employee_id
        del input_data.employee_id

        response = self.client.post(f"/employees/{employee_id}/assets", data=input_data.model_dump())
        return ToolResult(
            data=response,
            error=None
        )
