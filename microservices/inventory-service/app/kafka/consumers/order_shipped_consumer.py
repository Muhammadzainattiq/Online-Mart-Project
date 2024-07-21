import json
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from sqlmodel import select, Session
from app.db.db_connection import engine
from app.models.inventory_models import InventoryItem
from app.kafka.producer import produce_message, KAFKA_PRODUCER

async def consume_order_shipped_events(producer: AIOKafkaProducer):
    consumer = AIOKafkaConsumer(
        'order_shipped',

        bootstrap_servers='broker:19092',
        group_id="inventory_consuming_order_shipped",
        auto_offset_reset='earliest'
    )
    await consumer.start()
    try:
        async for msg in consumer:
            message = json.loads(msg.value.decode('utf-8'))
            print("Message Consumed in order_shipped>>>>>>>>>: ", message)
            await handle_order_shipped(message, producer)
    finally:
        await consumer.stop()

async def handle_order_shipped(order_data, producer: AIOKafkaProducer):
    print("order data: >>>>>", order_data)
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
                # Update stock_quantity based on the retrieved item
                if inventory_item.stock_quantity < item['quantity']:
                    print(f"Insufficient Stock for: {item}")
                    message_dict = {
                        "user_id": order_data["user_id"],
                        "order_id": order_data["order_id"],
                        "product_id": item['product_id'],
                        "color_id": item['color_id'],
                        "size_id": item['size_id'],
                        "order_quantity": item['quantity'],
                        "present_stock": inventory_item.stock_quantity,
                        "event_type": "insufficient_stock_information"
                    }
                    await produce_message("insufficient_stock_information", message_dict, producer)
                    continue
                else:
                    inventory_item.stock_quantity -= item['quantity']
                    session.add(inventory_item)
            else:
                print(f"Inventory Item Not Found for: {item}")

        session.commit()
