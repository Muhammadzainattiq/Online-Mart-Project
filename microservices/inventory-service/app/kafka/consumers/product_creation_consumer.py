from datetime import datetime
import json
from aiokafka import AIOKafkaConsumer
from sqlmodel import Session
from app.db.db_connection import engine
from app.models.inventory_models import InventoryItem

async def consume_product_creation_events():
    consumer = AIOKafkaConsumer(
        'product_creation',
        bootstrap_servers='broker:19092',
        group_id="inventory_consuming_product_creation",
        auto_offset_reset='earliest'
    )
    await consumer.start()
    try:
        async for msg in consumer:
            message = json.loads(msg.value.decode('utf-8'))
            print("Product Creation Message Consumed: ", message)
            handle_product_creation(message)
    finally:
        await consumer.stop()



def handle_product_creation(product_data):
    if not isinstance(product_data, dict):
        print("Invalid product creation data format")
        return

    required_fields = ['product_id', 'product_name', 'colors', 'sizes']
    if not all(field in product_data for field in required_fields):
        print("Missing required fields in product creation data")
        return

    with Session(engine) as session:
        for color in product_data['colors']:
            for size in product_data['sizes']:
                inventory_item = InventoryItem(
                    product_id=product_data['product_id'],
                    product_name=product_data['product_name'],
                    color_id=color['color_id'],
                    size_id=size['size_id'],
                    stock_quantity=0,
                    last_updated=datetime.now()
                )
                session.add(inventory_item)
        session.commit()


