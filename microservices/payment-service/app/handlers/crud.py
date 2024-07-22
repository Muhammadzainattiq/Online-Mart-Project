from typing import List, Optional
from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.payment_models import Payment, PaymentCreate, PaymentUser, PaymentStatus, PaymentMethod
from app.db.db_connection import engine

async def create_payment(payment_create: PaymentCreate, session: Session) -> Payment:
    payment = Payment.from_orm(payment_create)
    session.add(payment)
    session.commit()
    session.refresh(payment)
    return payment

async def get_payment_by_id(payment_id: int, session: Session) -> Payment:
    payment = session.get(Payment, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

async def update_payment_status(payment_id: int, status: PaymentStatus, session: Session, transaction_id: Optional[str] = None) -> Payment:
    payment = session.get(Payment, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    payment.status = status
    if transaction_id:
        payment.transaction_id = transaction_id
    session.add(payment)
    session.commit()
    session.refresh(payment)
    return payment

async def delete_payment(payment_id: int, session: Session):
    payment = session.get(Payment, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    session.delete(payment)
    session.commit()

async def create_payment_user(user_id: int, card_number: str, card_cvc: str, card_expiry: str, session: Session) -> PaymentUser:
    payment_user = PaymentUser(
        user_id=user_id,
        card_number=card_number,
        card_cvc=card_cvc,
        card_expiry=card_expiry
    )
    session.add(payment_user)
    session.commit()
    session.refresh(payment_user)
    return payment_user

async def read_all_user_payments(user_id: int, session: Session) -> PaymentUser:
    payment_user = session.get(PaymentUser, user_id)
    if not payment_user:
        raise HTTPException(status_code=404, detail="Payment user not found")
    return payment_user

async def update_payment_method(user_id: int, session: Session, card_number: Optional[str] = None, card_cvc: Optional[str] = None, card_expiry: Optional[str] = None) -> PaymentUser:
    payment_user = session.get(PaymentUser, user_id)
    if not payment_user:
        raise HTTPException(status_code=404, detail="Payment user not found")
    if card_number:
        payment_user.card_number = card_number
    if card_cvc:
        payment_user.card_cvc = card_cvc
    if card_expiry:
        payment_user.card_expiry = card_expiry
    session.add(payment_user)
    session.commit()
    session.refresh(payment_user)
    return payment_user

async def delete_payment_by_id(user_id: int, session: Session):
    payment_user = session.get(PaymentUser, user_id)
    if not payment_user:
        raise HTTPException(status_code=404, detail="Payment user not found")
    session.delete(payment_user)
    session.commit()

async def get_payments_by_user(user_id: int, session: Session) -> List[Payment]:
    statement = select(Payment).where(Payment.user_id == user_id)
    results = session.exec(statement)
    payments = results.all()
    if not payments:
        raise HTTPException(status_code=404, detail="No payments found for this user")
    return payments

async def read_all_payments(session: Session) -> List[Payment]:
    statement = select(Payment)
    results = session.exec(statement)
    payments = results.all()
    return payments
