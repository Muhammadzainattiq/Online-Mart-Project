from datetime import datetime
import json
from aiokafka import AIOKafkaConsumer
from sqlalchemy import select
from sqlmodel import Session
from app.models.inventory_models import InventoryItem
from app.db.db_connection import engine
async def consume_product_updation_events():
    consumer = AIOKafkaConsumer(
        'product_updation',
        bootstrap_servers='broker:19092',
        group_id="inventory_consuming_product_updation",
        auto_offset_reset='earliest'
    )
    await consumer.start()
    try:
        async for msg in consumer:
            message = json.loads(msg.value.decode('utf-8'))
            print("Product Updation Message Consumed: ", message)
            handle_product_updation(message)
    finally:
        await consumer.stop()


def handle_product_updation(event):
    product_id = event.get('product_id')
    product_name = event.get('product_name')

    if product_id is None or product_name is None:
        print("Missing product_id or product_name in product updation data")
        return

    with Session(engine) as session:
        result = session.exec(select(InventoryItem).where(InventoryItem.product_id == product_id))
        inventory_items = result.all()

        print("Inventory items: ", inventory_items)

        for inventory_item in inventory_items:
            (item,) = inventory_item
            print("Item details: ", item)  # Print the entire item to inspect its attributes
            print("Updating item: ", item)
            print("item.product_name: ", getattr(item, 'product_name'))  # Safely access product_name

            # Update item attributes
            setattr(item, 'product_name', product_name)
            item.last_updated = datetime.now()

        session.commit()
