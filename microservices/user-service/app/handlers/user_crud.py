from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Annotated
from app.models.user_models import User, UserUpdate, PaymentDetails, PaymentDetailsCreate
from app.db.db_connection import get_session, DB_SESSION
from app.kafka.producer import KAFKA_PRODUCER, produce_message
from app.utils import get_user_name_from_id
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



async def add_payment_details(user_id: int, payment_details: PaymentDetailsCreate, session:  DB_SESSION, producer: KAFKA_PRODUCER = KAFKA_PRODUCER):
    db_user = session.exec(select(User).where(User.user_id == user_id)).all()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_payment = PaymentDetails(user_id=user_id, **payment_details.model_dump())
    session.add(db_payment)
    session.commit()
    session.refresh(db_payment)
    user_name = await get_user_name_from_id(user_id)
    payment_details_dict = db_payment.model_dump()
    event_dict = {"event_type": "user_payment_details_added", "user_name": user_name,**payment_details_dict}
    await produce_message("user_payment_details_added", event_dict, producer)

    return db_payment


async def get_payment_details(user_id: int, session: DB_SESSION):
    db_statement = select(PaymentDetails).where(PaymentDetails.user_id == user_id)
    payment_details = session.exec(db_statement).first()
    if not payment_details:
        raise HTTPException(status_code=404, detail="Payment details not found")
    return payment_details