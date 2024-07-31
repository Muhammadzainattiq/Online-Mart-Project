from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.handlers.crud import (
    create_payment,
    get_payment_by_id,
    get_payments_by_user,
    update_payment_status,
    delete_payment,
    update_payment_method,
    read_all_payments
)
from app.models.payment_models import PaymentCreate, Payment, PaymentMethod, PaymentStatus
from app.db.db_connection import get_session

payment_router = APIRouter(prefix="/payment")

@payment_router.post('/add_payment', response_model=Payment)
async def create_payment_route(payment: PaymentCreate, session: Session = Depends(get_session)):
    return await create_payment(payment, session)

@payment_router.get('/get_payment_by_id/{payment_id}', response_model=Payment)
async def get_payment_by_id_route(payment_id: int, session: Session = Depends(get_session)):
    return await get_payment_by_id(payment_id, session)

@payment_router.get('/get_payment_by_user/{user_id}', response_model=List[Payment])
async def get_payments_by_user_route(user_id: int, session: Session = Depends(get_session)):
    return await get_payments_by_user(user_id, session)

@payment_router.put('/update_payment_status/{payment_id}', response_model=Payment)
async def update_payment_status_route(payment_id: int, status: PaymentStatus, session: Session = Depends(get_session)):
    return await update_payment_status(payment_id, status, session)

@payment_router.put('/update_payment_method/{payment_id}', response_model=Payment)
async def update_payment_method_route(payment_id: int, method: PaymentMethod, session: Session = Depends(get_session)):
    return await update_payment_method(payment_id, method, session)

@payment_router.delete('/delete_payment/{payment_id}')
async def delete_payment_by_id_route(payment_id: int, session: Session = Depends(get_session)):
    return await delete_payment(payment_id, session)


@payment_router.get('/read_all_payments', response_model=List[Payment])
async def read_all_payments_route(session: Session = Depends(get_session)):
    return await read_all_payments(session)

