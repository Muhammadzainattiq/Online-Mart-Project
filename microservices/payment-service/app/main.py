from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db_connection import create_tables
from app.user_routes import router

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
    return "Welcome to User Service"

# Include your routers or other configurations here
app.include_router(router)
