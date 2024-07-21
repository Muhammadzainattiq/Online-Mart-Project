from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Annotated
from app.models.user_models import User, UserUpdate
from app.db.db_connection import get_session, DB_SESSION
from app.kafka.producer import KAFKA_PRODUCER, produce_message
app = FastAPI()


router = APIRouter()


async def read_user_by_id(user_id: int, session: DB_SESSION):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def read_user_by_email(email: str, session: DB_SESSION):
    db_statement = select(User).where(User.user_email == email)
    user = session.exec(db_statement).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
async def get_all_users(session: DB_SESSION):
    users = session.exec(select(User)).all()
    return users


async def read_all_users(session: DB_SESSION):
    users = await get_all_users(session)
    return users


async def update_user_by_id(user_id: int, user_update: UserUpdate, session: DB_SESSION, producer: KAFKA_PRODUCER = KAFKA_PRODUCER):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields only if provided in user_update
    for field, value in user_update.model_dump().items():
        if value is not None:  # Skip updating if value is None if you will miss this it will give an error message 
            setattr(db_user, field, value)
    session.commit()
    session.refresh(db_user)
    updated_user_dict = db_user.model_dump()
    event_dict = {"event_type": "user_updation", "user_id": user_id,**updated_user_dict}
    await produce_message("user_updation", event_dict, producer)
    return db_user


async def delete_user_by_id(
    user_id: int,
    session: DB_SESSION,
    producer: KAFKA_PRODUCER = KAFKA_PRODUCER
):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete the user
    session.delete(db_user)
    session.commit()

    # Produce a Kafka event for user deletion
    message = {
        "user_id": user_id,
        "user_name": db_user.user_name,
        "user_email": db_user.user_email,
        "message": "User deleted successfully",
        "event_type": "user_deletion"
    }
    await produce_message("user_deletion", message, producer)

    return {"message": "User deleted successfully"}



app.include_router(router)
