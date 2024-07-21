from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.db_connection import create_tables
from app.routes.order_routes import order_router

# Lifespan context manager for FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating Tables")
    create_tables()
    print("Tables Created")
    try:
        yield
    finally:
        print("Lifespan context ended")

# Initialize FastAPI app with lifespan context
app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return "Welcome to Order Service"


@app.get("/health_check")
async def health_check():
   return {"status": "ok"}

# Include your routers or other configurations here
app.include_router(order_router)
