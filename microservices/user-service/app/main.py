from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.db_connection import create_tables
from app.routes.user_routes import user_router
from app.routes.user_auth_routes import user_auth_router
from app.routes.admin_auth_routes import admin_auth_router
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
async def home():
    return "Welcome to User Service"

@app.get("/user")
def home():
    return "Welcome to User Service"


@app.get("/user/health_check")
async def health_check():
   return {"service": "User",
       "status": "ok"}
      

# Include your routers or other configurations here
app.include_router(user_router)
app.include_router(user_auth_router)
app.include_router(admin_auth_router)
