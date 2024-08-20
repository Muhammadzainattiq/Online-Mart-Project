import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.db_connection import create_tables
from app.routes.order_routes import order_router
from app.kafka.consumer import consume_events
# Lifespan context manager for FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating Tables")
    create_tables()
    print("Tables Created")
    asyncio.create_task(consume_events())  # Start consuming Kafka events in the background thread
    try:
        yield
    finally:
        print("Lifespan context ended")

# Initialize FastAPI app with lifespan context
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def home():
    return "Welcome to Order Service"

@app.get("/order")
def home():
    return "Welcome to Order Service"


@app.get("/order/health_check")
async def health_check():
   return {"service": "Order",
       "status": "ok"}

# Include your routers or other configurations here
app.include_router(order_router)
