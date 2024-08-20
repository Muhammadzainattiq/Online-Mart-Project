import asyncio
from typing import List
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.models.notification_models import Notification, NotificationCreate
from sqlmodel import select
from app.db.db_connection import create_tables, DB_SESSION
from app.kafka.consumer import consume_events
from app.notification_utils import create_notification_and_send


# Lifespan context manager for FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating Tables")
    create_tables()
    print("Tables Created")
    asyncio.create_task(consume_events())
    try:
        yield
    finally:
        print("Lifespan context ended")

# Initialize FastAPI app with lifespan context
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def home():
    return "Welcome to Notification Service"

@app.get("/notification")
def home():
    return "Welcome to Notification Service"

@app.get("/notification/health_check")
async def health_check():
   return {"service": "Notification",
       "status": "ok"}


@app.get("/notifications/{user_id}", response_model=list[Notification])
async def get_notifications(user_id: int, session: DB_SESSION):
    notifications = session.exec(select(Notification).where(Notification.user_id == user_id)).all()
    if not notifications:
        raise HTTPException(status_code=404, detail="No notifications found for this user")
    return notifications



@app.post("/trigger_notification")
async def trigger_notification(notification : NotificationCreate):
    # notification = NotificationCreate(notification.user_id, notification.message)

    try:
        await create_notification_and_send(notification)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send notification: {str(e)}")
    
# Include your routers or other configurations here
# app.include_router(order_router)
