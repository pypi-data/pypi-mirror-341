"""Create order for warehouse tool."""

from typing import Optional, List

from pydantic import BaseModel, model_validator

from tools.base import BaseTool
from tools.result import ToolResult


class Product(BaseModel):
    """Product model for order."""
    id: int
    quantity: int

class CreateOrderForWarehouseInput(BaseModel):
    """Input for CreateOrderForWarehouseTool."""

    warehouse_id: int
    products: Optional[List[Product]] = None
    request_quote: Optional[bool] = None


class CreateOrderForWarehouseTool(BaseTool):
    """Tool for creating orders for warehouses."""

    @staticmethod
    def name() -> str:
        """The name of the tool."""
        return "create_order_for_warehouse"

    @staticmethod
    def description() -> str:
        """The description of the tool."""
        return """
Creates an order for the provided warehouse with the given data. To create it properly, you need the warehouse ID (which you can get with the `get_warehouses` tool), a list of product ids (which you can get with the `get_products` tool).

These are the fields you have to provide:
- warehouse_id: the id of the warehouse
- products: a list of products
    - products.*.id: the id of the product
    - products.*.quantity: the quantity of the product
- request_quote: whether the order will be a request for quote

You have to provide at least one product.

You should always confirm with the user that the information is correct before calling this tool.
"""

    async def execute(self, input_data: CreateOrderForWarehouseInput) -> ToolResult:
        """Execute the tool."""
        response = self.client.post(f"/warehouses/{input_data.warehouse_id}/orders", data=input_data.model_dump())
        return ToolResult(
            data=response,
            error=None
        )
