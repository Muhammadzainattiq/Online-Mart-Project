from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.handlers.order_crud import (create_order, read_order_by_order_id, read_order_by_user_id, read_all_orders, read_pending_orders, delete_order_by_id, update_order_status)
from app.models.order_models import Order
from app.db.db_connection import get_session

order_router = APIRouter(prefix="/order")

@order_router.post('/place_order')
async def place_order(placed_order: Annotated[Order, Depends(create_order)]):
    return placed_order

@order_router.get('/read_pending_orders/')
async def read_all_pending_orders(orders: Annotated[List[Order], Depends(read_pending_orders)]):
    return orders


@order_router.get('/read_order_by_order_id/{order_id}')
async def get_order_by_order_id(order: Annotated[Order, Depends(read_order_by_order_id)]):
    return order

@order_router.get('/read_order_by_user_id/{user_id}')
async def get_order_by_user_id(order: Annotated[Order, Depends(read_order_by_user_id)]):
    return order


@order_router.get('/read_all_orders')
async def get_all_orders(orders: Annotated[List[Order], Depends(read_all_orders)]):
    return orders

@order_router.delete('/{order_id}')
async def delete_order(message: Annotated[Order, Depends(delete_order_by_id,
)]):
    return message

@order_router.put('/update_order_status/{order_id}')
async def change_order_status(order: Annotated[Order, Depends(update_order_status)]):
    return order