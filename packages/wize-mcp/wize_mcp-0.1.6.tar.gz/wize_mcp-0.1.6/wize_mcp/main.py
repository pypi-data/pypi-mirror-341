from typing import Any
from mcp.server.fastmcp import FastMCP

from wize_mcp.tools.self import GetSelfTool
from wize_mcp.tools.assets import GetAssetsTool
from wize_mcp.tools.assets.get_assets import GetAssetsInput
from wize_mcp.tools.categories import GetCategoriesTool
from wize_mcp.tools.employees import GetEmployeesTool, CreateEmployeeTool, GetEmployeeUserTool, GetEmployeeAddressesTool, UpdateEmployeeTool, UpdateEmployeeAddressTool, CreateEmployeeAddressTool, CreateEmployeeAssetTool, CreateOrderForEmployeeTool
from wize_mcp.tools.employees.get_employees import GetEmployeesInput
from wize_mcp.tools.employees.create_employee import CreateEmployeeInput
from wize_mcp.tools.employees.get_employee_user import GetEmployeeUserInput
from wize_mcp.tools.employees.get_employee_addresses import GetEmployeeAddressesInput
from wize_mcp.tools.employees.update_employee import UpdateEmployeeInput
from wize_mcp.tools.employees.update_employee_address import UpdateEmployeeAddressInput
from wize_mcp.tools.employees.create_employee_address import CreateEmployeeAddressInput
from wize_mcp.tools.employees.create_employee_asset import CreateEmployeeAssetInput
from wize_mcp.tools.employees.create_order_for_employee import CreateOrderForEmployeeInput
from wize_mcp.tools.invites import CreateInviteTool
from wize_mcp.tools.invites.create_invite import CreateInviteInput
from wize_mcp.tools.offboards import GetOffboardsTool, CreateOffboardTool
from wize_mcp.tools.offboards.get_offboards import GetOffboardsInput
from wize_mcp.tools.offboards.create_offboard import CreateOffboardInput
from wize_mcp.tools.offices import GetOfficesTool, CreateOrderForOfficeTool
from wize_mcp.tools.offices.get_offices import GetOfficesInput
from wize_mcp.tools.offices.create_order_for_office import CreateOrderForOfficeInput
from wize_mcp.tools.orders import GetOrdersTool, GetOrderProductsTool, GetOrderShipmentsTool
from wize_mcp.tools.orders.get_orders import GetOrdersInput
from wize_mcp.tools.orders.get_order_products import GetOrderProductsInput
from wize_mcp.tools.orders.get_order_shipments import GetOrderShipmentsInput
from wize_mcp.tools.products import GetProductsTool
from wize_mcp.tools.products.get_products import GetProductsInput
from wize_mcp.tools.users import CreateUserTool
from wize_mcp.tools.users.create_user import CreateUserInput
from wize_mcp.tools.warehouses import GetWarehousesTool, CreateOrderForWarehouseTool
from wize_mcp.tools.warehouses.create_order_for_warehouse import CreateOrderForWarehouseInput
import dotenv

dotenv.load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("wize-mcp")

@mcp.tool(
    name=GetSelfTool.name(),
    description=GetSelfTool.description()
)
async def get_self():
    result = await GetSelfTool().execute()
    return result.to_response()

@mcp.tool(
    name=GetEmployeesTool.name(),
    description=GetEmployeesTool.description()
)
async def get_employees(input_data: GetEmployeesInput):
    result = await GetEmployeesTool().execute(input_data)
    return result.to_response()

@mcp.tool(
    name=GetOrdersTool.name(),
    description=GetOrdersTool.description()
)
async def get_orders(input_data: GetOrdersInput):
    result = await GetOrdersTool().execute(input_data)
    return result.to_response()

@mcp.tool(
    name=GetOrderProductsTool.name(),
    description=GetOrderProductsTool.description()
)
async def get_order_products(input_data: GetOrderProductsInput):
    result = await GetOrderProductsTool().execute(input_data)
    return result.to_response()

@mcp.tool(
    name=GetOrderShipmentsTool.name(),
    description=GetOrderShipmentsTool.description()
)
async def get_order_shipments(input_data: GetOrderShipmentsInput):
    result = await GetOrderShipmentsTool().execute(input_data)
    return result.to_response()

@mcp.tool(
    name=CreateEmployeeTool.name(),
    description=CreateEmployeeTool.description()
)
async def create_employee(input_data: CreateEmployeeInput):
    result = await CreateEmployeeTool().execute(input_data)
    return result.to_response()

@mcp.tool(
    name=GetEmployeeUserTool.name(),
    description=GetEmployeeUserTool.description()
)
async def get_employee_user(input_data: GetEmployeeUserInput):
    result = await GetEmployeeUserTool().execute(input_data)
    return result.to_response()

@mcp.tool(
    name=GetCategoriesTool.name(),
    description=GetCategoriesTool.description()
)
async def get_categories():
    result = await GetCategoriesTool().execute()
    return result.to_response()

@mcp.tool(
    name=GetOfficesTool.name(),
    description=GetOfficesTool.description()
)
async def get_offices(input_data: GetOfficesInput):
    result = await GetOfficesTool().execute(input_data)
    return result.to_response()

@mcp.tool(
    name=GetWarehousesTool.name(),
    description=GetWarehousesTool.description()
)
async def get_warehouses():
    result = await GetWarehousesTool().execute()
    return result.to_response()

@mcp.tool(
    name=GetProductsTool.name(),
    description=GetProductsTool.description()
)
async def get_products(input_data: GetProductsInput):
    result = await GetProductsTool().execute(input_data)
    return result.to_response()

@mcp.tool(
    name=GetOffboardsTool.name(),
    description=GetOffboardsTool.description()
)
async def get_offboards(input_data: GetOffboardsInput):
    result = await GetOffboardsTool().execute(input_data)
    return result.to_response()

@mcp.tool(
    name=GetAssetsTool.name(),
    description=GetAssetsTool.description()
)
async def get_assets(input_data: GetAssetsInput):
    result = await GetAssetsTool().execute(input_data)
    return result.to_response()

@mcp.tool(
    name=GetEmployeeAddressesTool.name(),
    description=GetEmployeeAddressesTool.description()
)
async def get_employee_addresses(input_data: GetEmployeeAddressesInput):
    result = await GetEmployeeAddressesTool().execute(input_data)
    return result.to_response()

@mcp.tool(
    name=UpdateEmployeeTool.name(),
    description=UpdateEmployeeTool.description()
)
async def update_employee(input_data: UpdateEmployeeInput):
    result = await UpdateEmployeeTool().execute(input_data)
    return result.to_response()

@mcp.tool(
    name=UpdateEmployeeAddressTool.name(),
    description=UpdateEmployeeAddressTool.description()
)
async def update_employee_address(input_data: UpdateEmployeeAddressInput):
    result = await UpdateEmployeeAddressTool().execute(input_data)
    return result.to_response()

@mcp.tool(
    name=CreateEmployeeAddressTool.name(),
    description=CreateEmployeeAddressTool.description()
)
async def create_employee_address(input_data: CreateEmployeeAddressInput):
    result = await CreateEmployeeAddressTool().execute(input_data)
    return result.to_response()

@mcp.tool(
    name=CreateEmployeeAssetTool.name(),
    description=CreateEmployeeAssetTool.description()
)
async def create_employee_asset(input_data: CreateEmployeeAssetInput):
    result = await CreateEmployeeAssetTool().execute(input_data)
    return result.to_response()

@mcp.tool(
    name=CreateInviteTool.name(),
    description=CreateInviteTool.description()
)
async def create_invite(input_data: CreateInviteInput):
    result = await CreateInviteTool().execute(input_data)
    return result.to_response()

@mcp.tool(
    name=CreateOffboardTool.name(),
    description=CreateOffboardTool.description()
)
async def create_offboard(input_data: CreateOffboardInput):
    result = await CreateOffboardTool().execute(input_data)
    return result.to_response()

@mcp.tool(
    name=CreateUserTool.name(),
    description=CreateUserTool.description()
)
async def create_user(input_data: CreateUserInput):
    result = await CreateUserTool().execute(input_data)
    return result.to_response()

@mcp.tool(
    name=CreateOrderForEmployeeTool.name(),
    description=CreateOrderForEmployeeTool.description()
)
async def create_order_for_employee(input_data: CreateOrderForEmployeeInput):
    result = await CreateOrderForEmployeeTool().execute(input_data)
    return result.to_response()

@mcp.tool(
    name=CreateOrderForOfficeTool.name(),
    description=CreateOrderForOfficeTool.description()
)
async def create_order_for_office(input_data: CreateOrderForOfficeInput):
    result = await CreateOrderForOfficeTool().execute(input_data)
    return result.to_response()

@mcp.tool(
    name=CreateOrderForWarehouseTool.name(),
    description=CreateOrderForWarehouseTool.description()
)
async def create_order_for_warehouse(input_data: CreateOrderForWarehouseInput):
    result = await CreateOrderForWarehouseTool().execute(input_data)
    return result.to_response()

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
