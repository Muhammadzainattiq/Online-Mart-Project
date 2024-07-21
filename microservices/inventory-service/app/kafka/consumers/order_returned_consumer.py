import json
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from sqlmodel import select, Session
from app.db.db_connection import engine
from app.models.inventory_models import InventoryItem

async def consume_order_returned_events():
    consumer = AIOKafkaConsumer(
        'order_returned',

        bootstrap_servers='broker:19092',
        group_id="inventory_consuming_order_returned",
        auto_offset_reset='earliest'
    )
    await consumer.start()
    try:
        async for msg in consumer:
            message = json.loads(msg.value.decode('utf-8'))
            print("Message Consumed in order_returned>>>>>>>>>: ", message)
            await handle_order_returned(message)
    finally:
        await consumer.stop()

async def handle_order_returned(order_data):
    with Session(engine) as session:
        for item in order_data['order_items']:
            inventory_item = session.exec(
                select(InventoryItem).where(
                    InventoryItem.product_id == item['product_id'],
                    InventoryItem.color_id == item['color_id'],
                    InventoryItem.size_id == item['size_id']
                )
            ).first()

            if inventory_item:
                print(f"Inventory Item Found: {inventory_item}")
                inventory_item.stock_quantity += item['quantity']
                session.add(inventory_item)
            else:
                print(f"Inventory Item Not Found for: {item}")

        session.commit()
