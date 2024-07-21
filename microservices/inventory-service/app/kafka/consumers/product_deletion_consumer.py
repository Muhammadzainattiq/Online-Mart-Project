import json
from aiokafka import AIOKafkaConsumer
from sqlalchemy import select
from sqlmodel import Session
from app.models.inventory_models import InventoryItem
from app.db.db_connection import engine

async def consume_product_deletion_events():
    consumer = AIOKafkaConsumer(
        'product_deletion',
        bootstrap_servers='broker:19092',
        group_id="inventory_consuming_product_deletion",
        auto_offset_reset='earliest'
    )
    await consumer.start()
    try:
        async for msg in consumer:
            message = json.loads(msg.value.decode('utf-8'))
            print("Product Deletion Message Consumed: ", message)
            handle_product_deletion(message)
    finally:
        await consumer.stop()



def handle_product_deletion(event):
    if not isinstance(event, dict):
        print("Invalid product deletion data format")
        return

    product_id = event.get('product_id')
    if product_id is None:
        print("Missing product_id in product deletion data")
        return

    with Session(engine) as session:
        inventory_items = session.exec(select(InventoryItem).where(InventoryItem.product_id == product_id)).all()
        for inventory_item in inventory_items:
            (item,) = inventory_item
            session.delete(item)
        session.commit()

