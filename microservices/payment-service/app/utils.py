from fastapi import HTTPException
from sqlmodel import Session
from app.db.db_connection import engine
from app.models.payment_models import PaymentUser
async def get_user_card_credentials(user_id):
    with Session(engine) as session:
        user_creds = session.get(PaymentUser, user_id)
        if user_creds:
            return user_creds
        else:
            raise HTTPException(status_code=404, detail="User not found")
        


async def perform_payment(user_card_creds, total_amount):
    # Implement payment processing logic here

    is_payment_successful = True

    return is_payment_successful


async def return_payment(user_card_creds, total_amount):
    # Implement refund/return logic here
    # For demonstration purposes, we'll just return the user's card details

    is_payment_returned_successful = True

    return is_payment_returned_successful