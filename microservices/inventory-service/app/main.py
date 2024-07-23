import asyncio
from datetime import datetime
import json
from typing import List
from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.models.inventory_models import InventoryItem, InventoryItemCreate
from sqlmodel import Session
from app.db.db_connection import DB_SESSION, create_tables, engine
from app.kafka.consumers.order_returned_consumer import consume_order_returned_events 
from app.kafka.consumers.order_shipped_consumer import consume_order_shipped_events 
from app.kafka.consumers.product_creation_consumer import consume_product_creation_events 
from app.kafka.consumers.product_deletion_consumer import consume_product_deletion_events 
from app.kafka.consumers.product_updation_consumer import consume_product_updation_events 
from app.kafka.producer import KAFKA_PRODUCER, init_kafka_producer, produce_message


# Lifespan context manager for FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating Tables")
    create_tables()
    print("Tables Created")
    producer = await init_kafka_producer()
    asyncio.create_task(consume_product_creation_events())
    asyncio.create_task(consume_product_deletion_events())
    asyncio.create_task(consume_product_updation_events())
    asyncio.create_task(consume_order_returned_events())
    asyncio.create_task(consume_order_shipped_events(producer=producer))
    try:
        yield
    finally:
        print("Lifespan context ended")

# Initialize FastAPI app with lifespan context
app = FastAPI(lifespan=lifespan)

@app.get("/inventory")
def home():
    return "Welcome to Inventory Service"

@app.get("/inventory/health_check")
async def health_check():
   return {"service": "Inventory",
       "status": "ok"}

@app.get("/inventory/read_inventory_item_by_id")
async def read_inventory_item(
    inventory_item_id: int,
    session: DB_SESSION
):
    db_item = session.get(InventoryItem, inventory_item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return db_item

@app.post("/inventory/add_stock")
async def add_stock(
    inventory_item_id: int,
    new_stock_quantity: int,
    session: DB_SESSION,
    producer: KAFKA_PRODUCER
):
    db_item = session.get(InventoryItem, inventory_item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    
    # Update the stock quantity
    db_item.stock_quantity += new_stock_quantity
    db_item.last_updated = datetime.now()
    session.commit()
    session.refresh(db_item)

    # Produce a Kafka event for adding stock
    message = {
        "inventory_item_id": inventory_item_id,
        "new_stock_quantity": new_stock_quantity,
        "updated_stock_quantity": db_item.stock_quantity,
        "timestamp": db_item.last_updated.isoformat(),
        "event_type": "stock_added"
    }
    await produce_message("stock_added", message, producer)

    return db_item

