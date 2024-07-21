
import asyncio
from fastapi import HTTPException
from sqlalchemy import select
from sqlmodel import Session
from app.db.db_connection import engine
from app.models.notification_models import NotificationCreate, Notification, NotificationUser
from app import settings

async def create_notification_and_send(notification: NotificationCreate):
    print("Starting create_notification_and_send function")
    
    notification_instance = Notification(**notification.model_dump())
    with Session(engine) as session:
        try:
            session.add(notification_instance)
            session.commit()
            session.refresh(notification_instance)
            print(f"Notification created: {notification_instance}")
        except Exception as e:
            session.rollback()
            print(f"Error creating notification: {str(e)}")
            return

    await asyncio.sleep(1)

    print("Fetching user email")
    try:
        user_email = await get_user_email_from_id(notification.user_id)
        print(f"User email fetched: {user_email}")
        
        print(f"Sending email to: {user_email}")
        await send_email(user_email, notification_instance.message)
        print(f"Email sent to: {user_email}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")


async def get_user_email_from_id(user_id):
    print(f"Fetching user details for user_id: {user_id}")
    with Session(engine) as session:
        try:
            user_details = session.get(NotificationUser, user_id)
            if user_details:
                print(f"User details retrieved: {user_details}")
                return user_details.user_email
            else:
                print(f"User with ID {user_id} not found")
                raise HTTPException(status_code=404, detail="User not found")
        except Exception as e:
            session.rollback()
            print(f"Error fetching user details: {str(e)}")
            raise



async def send_email(user_email, message):
  	#send email to user_email via a api
    pass


async def get_user_name_from_id(user_id):
    print(f"Fetching user details for user_id: {user_id}")
    with Session(engine) as session:
        try:
            user_details = session.get(NotificationUser, user_id)
            if user_details:
                print(f"User details retrieved: {user_details}")
                return user_details.user_name
            else:
                print(f"User with ID {user_id} not found")
                raise HTTPException(status_code=404, detail="User not found")
        except Exception as e:
            session.rollback()
            print(f"Error fetching user details: {str(e)}")
            raise