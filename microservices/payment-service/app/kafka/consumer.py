import json
import asyncio
from aiokafka import AIOKafkaConsumer
from sqlalchemy import select
from sqlmodel import Session
from app.db.db_connection import engine
from app.models.notification_models import NotificationCreate, NotificationUser
from app.notification_utils import create_notification_and_send

async def consume_events():
    consumer = AIOKafkaConsumer(
        'order_shipped',
        'order_returned',
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
    if event_type == "order_processing":
        await handle_order_processing(event)
    elif event_type == "order_returned":
        await handle_order_returned(event)


async def handle_order_processing(event):
    pass


async def handle_order_returned(event):
    pass