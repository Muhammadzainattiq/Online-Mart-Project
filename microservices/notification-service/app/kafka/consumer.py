import json
import asyncio
from aiokafka import AIOKafkaConsumer
from sqlalchemy import select
from sqlmodel import Session
from app.db.db_connection import engine
from app.models.notification_models import NotificationCreate, NotificationUser
from app.notification_utils import create_notification_and_send, get_user_name_from_id

async def consume_events():
    consumer = AIOKafkaConsumer(
        'user_creation',
        'user_updation',
        'user_deletion',
        'order_processing',
        'order_shipped',
        'order_delivered',
        'order_returned',
        'order_cancelled',
        'insufficient_stock_information',
        bootstrap_servers='broker:19092',
        group_id="notification_service_group",
        auto_offset_reset='earliest'
    )
    await consumer.start()
    try:
        async for msg in consumer:
            event = json.loads(msg.value.decode('utf-8'))
            print("Event Consumed: ", event)
            await handle_event(event)
    finally:
        await consumer.stop()

async def handle_event(event):
    event_type = event.get("event_type")
    if event_type == "user_creation":
        await handle_user_creation(event)
    elif event_type == "user_updation":
        await handle_user_updation(event)
    elif event_type == "user_deletion":
        await handle_user_deletion(event)
    elif event_type == "order_processing":
        await handle_order_processing(event)
    elif event_type == "order_shipped":
        await handle_order_shipped(event)
    elif event_type == "order_delivered":
        await handle_order_delivered(event)
    elif event_type == "order_returned":
        await handle_order_returned(event)
    elif event_type == "order_cancelled":
        await handle_order_cancelled(event)
    elif event_type == "insufficient_stock_information":
        await handle_insufficient_stock_information(event)

async def handle_user_creation(event):
    user_id = event.get('user_id')
    user_name = event.get('user_name')
    user_email = event.get('user_email')

    print("Creating user in database")
    with Session(engine) as session:
        user = NotificationUser(user_id=user_id, user_name=user_name, user_email=user_email)
        session.add(user)
        session.commit()
        session.refresh(user)
        print(f"User created: {user}")

    message = f"Welcome Dear Mr/Ms {user_name} to Zain's Online Store"
    notification = NotificationCreate(user_id=user_id, message=message)

    await create_notification_and_send(notification)

async def handle_user_updation(event):
    user_id = event.get('user_id')
    user_name = event.get('user_name')
    user_email = event.get('user_email')

    # Updating the notification user model
    with Session(engine) as session:
        notification_user = session.get(NotificationUser, user_id)
        if notification_user:
            # Ensure it is the correct instance type
            notification_user.user_email = user_email
            notification_user.user_name = user_name
            session.add(notification_user)
            session.commit()
            session.refresh(notification_user)
        else:
            print(f"User with ID {user_id} not found")

    message = f"Dear Mr/Ms {user_name}, your profile is updated"
    
    notification = NotificationCreate(user_id=user_id, message=message)
    await create_notification_and_send(notification)

async def handle_user_deletion(event):
    user_name = event.get('user_name')
    user_email = event.get('user_email')
    user_id = event.get('user_id')

    message = f"Sad to see you go Dear Mr/Ms {user_name}."

    notification = NotificationCreate(user_id=user_id, message=message)

    await create_notification_and_send(notification)

    with Session(engine) as session:
        notification_user = session.get(NotificationUser, user_id)
        if notification_user:
            session.delete(notification_user)
            session.commit()
        else:
            print(f"User with ID {user_id} not found")

    



async def handle_order_processing(event):
    order_id = event.get('order_id')
    user_id = event.get('user_id')
    order_date = event.get('order_date')
    shipping_address = event.get('shipping_address')
    total_amount = event.get('total_amount')
    order_items = event.get('order_items')
    
    if order_items is None:
        order_items = []

    # Constructing a detailed message
    order_items_details = "\n".join([
        f"Product ID: {item['product_id']}, Color ID: {item['color_id']}, Size ID: {item['size_id']}, Quantity: {item['quantity']}"
        for item in order_items
    ])

    user_name = await get_user_name_from_id(user_id)

    message = (
        f"Dear User {user_name},\n"
        f"Your order with ID {order_id} is now in processing.\n"
        f"Order Date: {order_date}\n"
        f"Shipping Address: {shipping_address}\n"
        f"Total Amount: ${total_amount}\n"
        f"Order Items:\n{order_items_details}\n"
        f"Status: Processing\n"
    )
    
    notification = NotificationCreate(user_id=user_id, message=message)
    await create_notification_and_send(notification)



async def handle_order_shipped(event):
    order_id = event.get('order_id')
    user_id = event.get('user_id')
    order_date = event.get('order_date')
    shipping_address = event.get('shipping_address')
    total_amount = event.get('total_amount')
    order_items = event.get('order_items')

    if order_items is None:
        order_items = []

    # Constructing a detailed message
    order_items_details = "\n".join([
        f"Product ID: {item['product_id']}, Color ID: {item['color_id']}, Size ID: {item['size_id']}, Quantity: {item['quantity']}"
        for item in order_items
    ])

    user_name = await get_user_name_from_id(user_id)
    
    message = (
        f"Dear User {user_name},\n"
        f"Your order with ID {order_id} is shipped.\n"
        f"Order Date: {order_date}\n"
        f"Shipping Address: {shipping_address}\n"
        f"Total Amount: ${total_amount}\n"
        f"Order Items:\n{order_items_details}\n"
        f"Status: Shipped\n"
    )


    notification = NotificationCreate(user_id=user_id, message=message)
    await create_notification_and_send(notification)



async def handle_order_delivered(event):
    order_id = event.get('order_id')
    user_id = event.get('user_id')
    order_date = event.get('order_date')
    shipping_address = event.get('shipping_address')
    total_amount = event.get('total_amount')
    order_items = event.get('order_items')
    
    if order_items is None:
            order_items = []

    # Constructing a detailed message
    order_items_details = "\n".join([
        f"Product ID: {item['product_id']}, Color ID: {item['color_id']}, Size ID: {item['size_id']}, Quantity: {item['quantity']}"
        for item in order_items
    ])
    
    user_name = await get_user_name_from_id(user_id)

    message = (
        f"Dear User {user_name},\n"
        f"Your order with ID {order_id} has been successfully delivered.\n"
        f"Order Date: {order_date}\n"
        f"Shipping Address: {shipping_address}\n"
        f"Total Amount: ${total_amount}\n"
        f"Order Items:\n{order_items_details}\n"
        f"Status: Delivered\n"
    )

    notification = NotificationCreate(user_id=user_id, message=message)
    await create_notification_and_send(notification)




async def handle_order_returned(event):
    order_id = event.get('order_id')
    user_id = event.get('user_id')
    order_date = event.get('order_date')
    shipping_address = event.get('shipping_address')
    total_amount = event.get('total_amount')
    order_items = event.get('order_items')
    
    if order_items is None:
        order_items = []

    # Constructing a detailed message
    order_items_details = "\n".join([
        f"Product ID: {item['product_id']}, Color ID: {item['color_id']}, Size ID: {item['size_id']}, Quantity: {item['quantity']}"
        for item in order_items
    ])
    
    user_name = await get_user_name_from_id(user_id)

    message = (
        f"Dear User {user_name},\n"
        f"Your order with ID {order_id} is returned successfully.\n"
        f"Order Date: {order_date}\n"
        f"Shipping Address: {shipping_address}\n"
        f"Total Amount: ${total_amount}\n"
        f"Order Items:\n{order_items_details}\n"
        f"Status: Returned\n"
    )

    notification = NotificationCreate(user_id=user_id, message=message)
    await create_notification_and_send(notification)


async def handle_order_cancelled(event):
    order_id = event.get('order_id')
    user_id = event.get('user_id')
    order_date = event.get('order_date')
    shipping_address = event.get('shipping_address')
    total_amount = event.get('total_amount')
    order_items = event.get('order_items')
    
    if order_items is None:
        order_items = []


    # Constructing a detailed message
    order_items_details = "\n".join([
        f"Product ID: {item['product_id']}, Color ID: {item['color_id']}, Size ID: {item['size_id']}, Quantity: {item['quantity']}"
        for item in order_items
    ])
    
    user_name = await get_user_name_from_id(user_id)

    message = (
        f"Dear User {user_name},\n"
        f"Your order with ID {order_id} is cancelled successfully.\n"
        f"Order Date: {order_date}\n"
        f"Shipping Address: {shipping_address}\n"
        f"Total Amount: ${total_amount}\n"
        f"Order Items:\n{order_items_details}\n"
        f"Status: Cancelled\n"
    )

    notification = NotificationCreate(user_id=user_id, message=message)
    await create_notification_and_send(notification)


async def handle_insufficient_stock_information(event):
    user_id = event.get('user_id')
    order_id = event.get('order_id')
    product_id = event.get('product_id')
    color_id = event.get('color_id')
    size_id = event.get('size_id')
    order_quantity = event.get('order_quantity')
    present_stock = event.get('present_stock')
    
    user_name = await get_user_name_from_id(user_id)

    # Constructing a detailed message
    message = (
        f"Dear User {user_name},\n"
        f"Unfortunately, we do not have enough stock to fulfill your order with ID {order_id}.\n"
        f"Order Details:\n"
        f"  - Product ID: {product_id}\n"
        f"  - Color ID: {color_id}\n"
        f"  - Size ID: {size_id}\n"
        f"  - Ordered Quantity: {order_quantity}\n"
        f"  - Available Stock: {present_stock}\n"
        f"Please update your order or contact our support team for further assistance.\n"
    )

    notification = NotificationCreate(user_id=user_id, message=message)
    await create_notification_and_send(notification)