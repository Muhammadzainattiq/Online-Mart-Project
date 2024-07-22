import json
import asyncio
from aiokafka import AIOKafkaConsumer
from sqlmodel import Session, select
from app.db.db_connection import engine 
from app.models.order_models import Order, OrderStatus
from app.handlers.order_crud import update_order_status
from app.kafka.producer import KAFKA_PRODUCER, produce_message

async def consume_events():
    consumer = AIOKafkaConsumer(
        'payment_successful',
        'payment_failed',
        bootstrap_servers='broker:19092',
        group_id="order_service_group",
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
    if event_type == "payment_successful":
        await handle_payment_successful(event)
    elif event_type == "payment_failed":
        await handle_payment_failed(event)

async def handle_payment_successful(event):
    order_id = event.get("order_id")
    with Session(engine) as session:
        await update_order_status(session, order_id, OrderStatus.SHIPPED)


async def handle_payment_failed(event):
    order_id = event.get("order_id")
    with Session(engine) as session:
        await update_order_status(session, order_id, OrderStatus.PENDING)
