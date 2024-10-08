import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.db_connection import create_tables
from app.routes.payment_routes import payment_router
from app.kafka.consumer import consume_events
from app.kafka.producer import KAFKA_PRODUCER, init_kafka_producer
# Lifespan context manager for FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating Tables")
    create_tables()
    print("Tables Created")
    producer = await init_kafka_producer()
    asyncio.create_task(consume_events(producer = producer))
    try:
        yield
    finally:
        print("Lifespan context ended")

# Initialize FastAPI app with lifespan context
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def home():
    return "Welcome to Payment Service"

@app.get("/payment")
def home():
    return "Welcome to Payment Service"


@app.get("/payment/health_check")
def health_check():
    return {"service": "Payment",
        "status": "ok"}

# Include your routers or other configurations here
app.include_router(payment_router)
