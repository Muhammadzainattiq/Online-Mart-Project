from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.db_connection import create_tables
from app.routes.product_crud_routes import product_router
from app.routes.category_crud_routes import category_router

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
    return "Welcome to Product Service"


@app.get("/health_check")
async def health_check():
   return {"status": "ok"}

# Include your routers or other configurations here
app.include_router(product_router)
app.include_router(category_router)
