"""Create order for office tool."""

from typing import Optional, List

from pydantic import BaseModel, model_validator

from tools.base import BaseTool
from tools.result import ToolResult


class Product(BaseModel):
    """Product model for order."""
    id: int
    quantity: int
    budget_category_id: Optional[int] = None

class Asset(BaseModel):
    """Asset model for order."""
    id: int
    budget_deduction: Optional[float] = None

class CreateOrderForOfficeInput(BaseModel):
    """Input for CreateOrderForOfficeTool."""

    office_id: int
    assigned_to: int
    delivery_with_express: Optional[bool] = None
    products: Optional[List[Product]] = None
    address_id: Optional[int] = None
    assets: Optional[List[Asset]] = None
    tax_identification_number: Optional[str] = None

    @model_validator(mode='after')
    def validate_model(self) -> 'CreateOrderForOfficeInput':
        """Validate that either products or assets are provided."""
        if not self.products and not self.assets:
            raise ValueError('Either products or assets must be provided')
        return self


class CreateOrderForOfficeTool(BaseTool):
    """Tool for creating orders for offices."""

    @staticmethod
    def name() -> str:
        """The name of the tool."""
        return "create_order_for_office"

    @staticmethod
    def description() -> str:
        """The description of the tool."""
        return """
Creates an order for the provided office with the given data. To create it properly, you need the office ID (which you can get with the `get_offices` tool), a list of product ids, an address id (which you can get with the `get_office_addresses` tool) and a list of asset ids (which you can get with the `get_office_assets` tool).

These are the fields you have to provide:
- office_id: the id of the office
- assigned_to: the id of the employee that will receive the order in that office
- products: a list of products
    - products.*.id: the id of the product
    - products.*.quantity: the quantity of the product
    - products.*.budget_category_id: the id of the budget category of the product
- address_id: the id of the address
- assets: a list of assets
    - assets.*.id: the id of the asset
    - assets.*.budget_deduction: the budget deduction of the asset
- tax_identification_number: the tax identification number of the employee
- delivery_with_express: whether the order will be delivered with express

You have to provide at least one product or one asset.

You should always confirm with the user that the information is correct before calling this tool.
"""

    async def execute(self, input_data: CreateOrderForOfficeInput) -> ToolResult:
        """Execute the tool."""
        data = input_data.model_dump()
        if 'assets' not in data or data['assets'] is None:
            data['assets'] = []
        if 'products' not in data or data['products'] is None:
            data['products'] = []

        response = self.client.post(f"/offices/{input_data.office_id}/orders", data=data)
        return ToolResult(
            data=response,
            error=None
        )
