"""Get order shipments tool."""

from typing import Union

from pydantic import BaseModel

from tools.base import BaseTool
from tools.result import ToolResult


class GetOrderShipmentsInput(BaseModel):
    """Input for GetOrderShipmentsTool."""
    order_number: Union[str, int]


class GetOrderShipmentsTool(BaseTool):
    """Tool for getting order shipments."""

    @staticmethod
    def name() -> str:
        """The name of the tool."""
        return "get_order_shipments"

    @staticmethod
    def description() -> str:
        """The description of the tool."""
        return """
Get a list of shipments for a specific order.

You have to provide:
- order_number: the number of the order. You can use this parameter to search for a specific order

"""

    async def execute(self, input_data: GetOrderShipmentsInput) -> ToolResult:
        """Execute the tool."""
        response = self.client.get(f'/orders/{input_data.order_number}/shipments')
        return ToolResult(
            data=response,
            error=None
        )
