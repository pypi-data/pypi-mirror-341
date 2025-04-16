import importlib.util
import asyncio

# Specify the file path
file_path = './wize-mcp.py'

# Create a module spec from the file path
spec = importlib.util.spec_from_file_location("wize_mcp", file_path)

# Create a new module based on the spec
wize_mcp = importlib.util.module_from_spec(spec)

# Execute the module
spec.loader.exec_module(wize_mcp)

# Now you can use the module
# For example, if the module has a function called `my_function`, you can call it like this:

response_self = asyncio.run(wize_mcp.get_self())
if 'id' in response_self:
    print('✅ Self fetched successfully')
else:
    print('❌ Failed to fetch self')

response1 = asyncio.run(wize_mcp.get_employees(wize_mcp.GetEmployeesInput()))
if len(response1) > 0:
    print('✅ Employees fetched successfully')
else:
    print('❌ Failed to fetch employees')

response1 = asyncio.run(wize_mcp.get_employees(wize_mcp.GetEmployeesInput(
    email='john.doe2@workwize.com'
)))
if len(response1) > 0:
    print('✅ Employees fetched successfully')
else:
    print('❌ Failed to fetch employees')

response2 = asyncio.run(wize_mcp.get_offices(wize_mcp.GetOfficesInput()))
if len(response2) > 0:
    print('✅ Offices fetched successfully')
else:
    print('❌ Failed to fetch offices')

response3 = asyncio.run(wize_mcp.get_warehouses())
if len(response3) > 0:
    print('✅ Warehouses fetched successfully')
else:
    print('❌ Failed to fetch warehouses')

response4 = asyncio.run(wize_mcp.get_orders(wize_mcp.GetOrdersInput()))
if len(response4) > 0:
    print('✅ Orders fetched successfully')
else:
    print('❌ Failed to fetch orders')

response5 = asyncio.run(wize_mcp.get_order_products(wize_mcp.GetOrderProductsInput(order_number=response4['data'][0]['number'])))
if len(response5) > 0:
    print('✅ Order products fetched successfully')
else:
    print('❌ Failed to fetch order products')

response6 = asyncio.run(wize_mcp.get_order_shipments(wize_mcp.GetOrderShipmentsInput(order_number=response4['data'][0]['number'])))
if len(response6) > 0:
    print('✅ Order shipments fetched successfully')
else:
    print('❌ Failed to fetch order shipments')

response7 = asyncio.run(wize_mcp.get_products(wize_mcp.GetProductsInput()))
if len(response7) > 0:
    print('✅ Products fetched successfully')
else:
    print('❌ Failed to fetch products')

response7 = asyncio.run(wize_mcp.get_products(wize_mcp.GetProductsInput(search='macbook')))
if len(response7) > 0:
    print('✅ Products fetched successfully')
else:
    print('❌ Failed to fetch products')

response8 = asyncio.run(wize_mcp.get_offboards(wize_mcp.GetOffboardsInput()))
if len(response8['data']) > 0:
    print('✅ Offboards fetched successfully')
else:
    print('❌ Failed to fetch offboards')

response9 = asyncio.run(wize_mcp.get_employee_user(wize_mcp.GetEmployeeUserInput(employee_id=response1[0]['id'])))
if 'id' in response9:
    print('✅ Employee user fetched successfully')
else:
    print('❌ Failed to fetch employee user')

response10 = asyncio.run(wize_mcp.get_employee_addresses(wize_mcp.GetEmployeeAddressesInput(employee_id=response1[0]['id'])))
if 'id' in response10['data']:
    print('✅ Employee addresses fetched successfully')
else:
    print('❌ Failed to fetch employee addresses')

response11 = asyncio.run(wize_mcp.get_assets(wize_mcp.GetAssetsInput(employee_id=response1[0]['id'])))
if len(response11['data']) > 0:
    print('✅ Assets fetched successfully')
else:
    print('❌ Failed to fetch assets')

response12 = asyncio.run(wize_mcp.get_categories())
if len(response12) > 0:
    print('✅ Categories fetched successfully')
else:
    print('❌ Failed to fetch categories')

response13 = asyncio.run(wize_mcp.get_offices(wize_mcp.GetOfficesInput()))
if len(response13) > 0:
    print('✅ Offices fetched successfully')
else:
    print('❌ Failed to fetch offices')

# response14 = asyncio.run(wize_mcp.create_employee(wize_mcp.CreateEmployeeInput(
#     role='Sales',
#     given_name='John',
#     last_name='Doe',
#     email='john.doe@example.com',
#     phone_number='1234567890',
#     is_notified=True
# )))
# if 'id' in response14:
#     print('✅ Employee created successfully')
# else:
#     print('❌ Failed to create employee')

# response15 = asyncio.run(wize_mcp.update_employee(wize_mcp.UpdateEmployeeInput(
#     employee_id=response14['employee_id'],
#     email='john.doe2@example.com',
# )))
# if 'id' in response15:
#     print('✅ Employee updated successfully')
# else:
#     print('❌ Failed to update employee')

# response16 = asyncio.run(wize_mcp.create_employee_address(wize_mcp.CreateEmployeeAddressInput(
#     employee_id=response14['employee_id'],
#     company_name='Wize',
#     address_line_1='1234 Main St',
#     address_line_2='Anytown',
#     additional_address_line='USA',
#     city='Anytown',
#     region='USA',
#     postal_code='12345',
#     country_id=1,
#     phone_number='1234567890',
#     email='john.doe@example.com',
#     name='John',
#     last_name='Doe'
# )))

# if 'id' in response16['data']:
#     print('✅ Employee address created successfully')
# else:
#     print('❌ Failed to create employee address')

# response17 = asyncio.run(wize_mcp.update_employee_address(wize_mcp.UpdateEmployeeAddressInput(
#     employee_id=response14['employee_id'],
#     address_id=response16['data']['id'],
#     email='john.doe3@example.com',
# )))

# if 'id' in response17['data']:
#     print('✅ Employee address updated successfully')
# else:
#     print('❌ Failed to update employee address')


# response18 = asyncio.run(wize_mcp.create_order_for_office(wize_mcp.CreateOrderForOfficeInput(
#     office_id=15,
#     assigned_to=response14['employee_id'],
#     products=[{'id': 58694, 'quantity': 1}],
#     address_id=response16['data']['id'],
# )))

# if 'id' in response18['data']:
#     print('✅ Order created successfully')
# else:
#     print('❌ Failed to create order')
