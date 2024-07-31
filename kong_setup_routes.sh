#!/bin/bash
# ++++++++++++++++++++++++++++++++++++++++++user service +++++++++++++++++++++++++++++++++++++++++++++++++

# =====================================user_routes============================================
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/user" \
    --data "service.name=user_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=home_user_route"

curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/user/health_check" \
    --data "service.name=user_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=user_health_check_route"

curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/user/add_user_payment_details" \
    --data "service.name=user_service" \
    --data "methods[]=POST" \
    --data "strip_path=false" \
    --data "name=add_user_payment_details_route"

curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/user/get_payment_details/{user_id}" \
    --data "service.name=user_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=get_payment_details_route"

curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/user/get_user_by_id/{user_id}" \
    --data "service.name=user_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=get_user_by_id_route"

curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/user/get_user_by_email/{email}" \
    --data "service.name=user_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=get_user_by_email_route"

curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/user/get_all_users" \
    --data "service.name=user_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=get_all_users_route"

curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/user/delete_user/{user_id}" \
    --data "service.name=user_service" \
    --data "methods[]=DELETE" \
    --data "strip_path=false" \
    --data "name=delete_user_route"

curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/user/update_user/{user_id}" \
    --data "service.name=user_service" \
    --data "methods[]=PUT" \
    --data "strip_path=false" \
    --data "name=update_user_route"

curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/user/add_user_payment_details" \
    --data "service.name=user_service" \
    --data "methods[]=POST" \
    --data "strip_path=false" \
    --data "name=add_user_payment_details_route"

# =======================================user_auth_routes =================================================

#!/bin/bash

# Signup user route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/user_auth/signup_user/" \
    --data "service.name=user_service" \
    --data "methods[]=POST" \
    --data "strip_path=false" \
    --data "name=signup_user_route"

# Login user route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/user_auth/login_user/" \
    --data "service.name=user_service" \
    --data "methods[]=POST" \
    --data "strip_path=false" \
    --data "name=login_user_route"

# Get user route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/user_auth/get_user/" \
    --data "service.name=user_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=get_user_route"


==============================================user_auth_routes============================================

#!/bin/bash

# Signup admin route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/admin_auth/signup_admin" \
    --data "service.name=user_service" \
    --data "methods[]=POST" \
    --data "strip_path=false" \
    --data "name=signup_admin_route"

# Login admin route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/admin_auth/login_admin" \
    --data "service.name=user_service" \
    --data "methods[]=POST" \
    --data "strip_path=false" \
    --data "name=login_admin_route"

# Get admin route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/admin_auth/get_admin" \
    --data "service.name=user_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=get_admin_route"

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++ user_service +++++++++++++++++++++++++++++++++++++++++++++


# +++++++++++++++++++++++++++++++++++++++++++++++++++++ product service ++++++++++++++++++++++++++++++++++++++++++++


# =====================================================product crud ================================================

#!/bin/bash

curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/product" \
    --data "service.name=product_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=home_product_route"

curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/product/health_check" \
    --data "service.name=product_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=product_health_check_route"

# Add product route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/product/add_product" \
    --data "service.name=product_service" \
    --data "methods[]=POST" \
    --data "strip_path=false" \
    --data "name=add_product_route"

# Read product by ID route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/product/read_product_by_id/{product_id}" \
    --data "service.name=product_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=read_product_by_id_route"

# Read products by name route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/product/read_products_by_name/{name}" \
    --data "service.name=product_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=read_products_by_name_route"

# Read products by category route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/product/read_products_by_category/{category}" \
    --data "service.name=product_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=read_products_by_category_route"

# Read all products route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/product/read_all_products" \
    --data "service.name=product_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=read_all_products_route"

# Read all products with pagination route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/product/read_all_products_with_pagination" \
    --data "service.name=product_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=read_all_products_with_pagination_route"

# Delete product route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/product/delete_product/{product_id}" \
    --data "service.name=product_service" \
    --data "methods[]=DELETE" \
    --data "strip_path=false" \
    --data "name=delete_product_route"

# Update product route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/product/update_product/{product_id}" \
    --data "service.name=product_service" \
    --data "methods[]=PUT" \
    --data "strip_path=false" \
    --data "name=update_product_route"



=======================================================category_crud ============================================

# Add category route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/category/add_category" \
    --data "service.name=product_service" \
    --data "methods[]=POST" \
    --data "strip_path=false" \
    --data "name=add_category_route"

# Delete category route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/category/delete_category/{category_id}" \
    --data "service.name=product_service" \
    --data "methods[]=DELETE" \
    --data "strip_path=false" \
    --data "name=delete_category_route"

# Update category route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/category/update_category/{category_id}" \
    --data "service.name=product_service" \
    --data "methods[]=PUT" \
    --data "strip_path=false" \
    --data "name=update_category_route"


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ product service ++++++++++++++++++++++++++++++++++++++++++++



# +++++++++++++++++++++++++++++++++++++++++++++++++++++++ order service +++++++++++++++++++++++++++++++++++++++++++++

curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/order" \
    --data "service.name=order_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=home_order_route"

curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/order/health_check" \
    --data "service.name=order_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=order_health_check_route"

# Place order route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/order/place_order" \
    --data "service.name=order_service" \
    --data "methods[]=POST" \
    --data "strip_path=false" \
    --data "name=place_order_route"

# Read pending orders route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/order/read_pending_orders/" \
    --data "service.name=order_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=read_pending_orders_route"

# Read order by order ID route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/order/read_order_by_order_id/{order_id}" \
    --data "service.name=order_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=read_order_by_order_id_route"

# Read order by user ID route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/order/read_order_by_user_id/{user_id}" \
    --data "service.name=order_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=read_order_by_user_id_route"

# Read all orders route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/order/read_all_orders" \
    --data "service.name=order_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=read_all_orders_route"

# Delete order route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/order/{order_id}" \
    --data "service.name=order_service" \
    --data "methods[]=DELETE" \
    --data "strip_path=false" \
    --data "name=delete_order_route"


# Update order status route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/order/update_order_status/{order_id}" \
    --data "service.name=order_service" \
    --data "methods[]=PUT" \
    --data "strip_path=false" \
    --data "name=update_order_status_route"


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++ order service +++++++++++++++++++++++++++++++++++++++++++++


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++ inventory service +++++++++++++++++++++++++++++++++++++++++++++


curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/inventory" \
    --data "service.name=inventory_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=home_inventory_route"

curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/inventory/health_check" \
    --data "service.name=inventory_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=inventory_health_check_route"

curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/inventory/read_inventory_item_by_id" \
    --data "service.name=inventory_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=read_inventory_item_route"

curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/inventory/add_stock" \
    --data "service.name=inventory_service" \
    --data "methods[]=POST" \
    --data "strip_path=false" \
    --data "name=add_stock_route"

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++ notification service +++++++++++++++++++++++++++++++++++++++++++

# Home route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/notification" \
    --data "service.name=notification_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=home_notification_route"

# Health check route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/notification/health_check" \
    --data "service.name=notification_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=notification_health_check_route"

# Get notifications by user ID route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/notifications/{user_id}" \
    --data "service.name=notification_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=get_notifications_route"

# Trigger notification route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/trigger_notification" \
    --data "service.name=notification_service" \
    --data "methods[]=POST" \
    --data "strip_path=false" \
    --data "name=trigger_notification_route"


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++ notification service +++++++++++++++++++++++++++++++++++++++


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++ payment service ++++++++++++++++++++++++++++++++++++++++++++

# Home route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/payment" \
    --data "service.name=payment_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=home_payment_route"

# Health check route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/payment/health_check" \
    --data "service.name=payment_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=payment_health_check_route"

# Add Payment Route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/payment/add_payment" \
    --data "service.name=payment_service" \
    --data "methods[]=POST" \
    --data "strip_path=false" \
    --data "name=add_payment_route"

# Get Payment by ID Route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/payment/get_payment_by_id/{payment_id}" \
    --data "service.name=payment_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=get_payment_by_id_route"

# Get Payments by User ID Route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/payment/payments/user/{user_id}" \
    --data "service.name=payment_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=get_payments_by_user_route"

# Update Payment Status Route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/payment/payments/{payment_id}/status" \
    --data "service.name=payment_service" \
    --data "methods[]=PUT" \
    --data "strip_path=false" \
    --data "name=update_payment_status_route"

# Update Payment Method Route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/payment/payments/{payment_id}/method" \
    --data "service.name=payment_service" \
    --data "methods[]=PUT" \
    --data "strip_path=false" \
    --data "name=update_payment_method_route"

# Delete Payment by ID Route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/payment/payments/{payment_id}" \
    --data "service.name=payment_service" \
    --data "methods[]=DELETE" \
    --data "strip_path=false" \
    --data "name=delete_payment_by_id_route"

# Read All Payments Route
curl -i -X POST http://localhost:8001/routes \
    --data "paths[]=/payment/payments" \
    --data "service.name=payment_service" \
    --data "methods[]=GET" \
    --data "strip_path=false" \
    --data "name=read_all_payments_route"


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++ payment service ++++++++++++++++++++++++++++++++++++++++++++