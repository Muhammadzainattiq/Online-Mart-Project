from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import datetime

from app.models.order_models import Order, OrderItem, OrderCreate, OrderStatus, PaymentMethod
from app.db.db_connection import get_session, DB_SESSION
from app.kafka.producer import produce_message, KAFKA_PRODUCER
router = APIRouter()

async def create_order(order: OrderCreate, session: DB_SESSION, producer: KAFKA_PRODUCER):
    db_order = Order(
        user_id=order.user_id,
        order_date=datetime.now(),
        shipping_address=order.shipping_address,
        total_amount=sum(item.price_per_unit * item.quantity for item in order.order_items),
        payment_method=order.payment_method,
        order_items=[
            OrderItem(
                product_id=item.product_id,
                color_id=item.color_id,
                size_id=item.size_id,
                quantity=item.quantity,
                price_per_unit=item.price_per_unit
            ) for item in order.order_items
        ]
    )
    session.add(db_order)
    session.commit()
    session.refresh(db_order)

    # # Payment Processing
    # if db_order.payment_method == PaymentMethod.PAY_FAST:
    #     process_payfast_payment(db_order)  # Implement Pay Fast payment processing
    # elif db_order.payment_method == PaymentMethod.STRIPE:
    #     process_stripe_payment(db_order)  # Implement Stripe payment processing

    # Producing new_order_creation event
    order_message_dict = {
        "user_id": order.user_id,
        "order_id": db_order.order_id,
        "payment_method": order.payment_method,
        "order_items": [
            {
                "product_id": item.product_id,
                "color_id": item.color_id,
                "size_id": item.size_id,
                "quantity": item.quantity
            } for item in db_order.order_items
        ],
        "event_type": "order_creation"
    }
    await produce_message("order_creation", order_message_dict, producer)
    return db_order

def read_order_by_order_id(order_id: int, session: DB_SESSION):
    order = session.exec(select(Order).where(Order.order_id == order_id)).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def read_order_by_user_id(user_id: int, session: DB_SESSION):
    order = session.exec(select(Order).where(Order.user_id == user_id)).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found for that user")
    return order

def read_pending_orders(session: DB_SESSION):
    orders = session.exec(select(Order).where(Order.order_status == OrderStatus.PENDING)).all()
    return orders

async def read_all_orders(session: DB_SESSION):
    orders = session.exec(select(Order)).all()
    return orders

async def delete_order_by_id(order_id: int, session: DB_SESSION):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    session.delete(db_order)
    session.commit()
    return {"message": "Order deleted successfully"}

async def update_order_status(
    order_id: int,
    status: OrderStatus,
    session: DB_SESSION,
    producer: KAFKA_PRODUCER
):
    # Fetch the order from the database
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update the order status
    db_order.order_status = status
    # Commit the changes to the database
    session.commit()
    session.refresh(db_order)

    order_items = [
        {
            "product_id": item.product_id,
            "color_id": item.color_id,
            "size_id": item.size_id,
            "quantity": item.quantity
        } for item in db_order.order_items
    ]

    order_date_iso = db_order.order_date.isoformat()

    status_update_dict = {
        "order_id": db_order.order_id,
        "user_id": db_order.user_id,
        "order_date": order_date_iso,
        "shipping_address": db_order.shipping_address,
        "total_amount": db_order.total_amount,
        "order_items": order_items,
        "status": status.value,
        "payment_method": db_order.payment_method
    }

    # Produce different events based on the status
    if status == OrderStatus.PENDING:
        event_dict = {"event_type": "order_pending", **status_update_dict}
        await produce_message("order_pending", event_dict, producer)
    elif status == OrderStatus.PROCESSING:
        event_dict = {"event_type": "order_processing", **status_update_dict}
        await produce_message("order_processing", event_dict, producer)
    elif status == OrderStatus.SHIPPED:
        event_dict = {"event_type": "order_shipped", **status_update_dict}
        await produce_message("order_shipped", event_dict, producer)
    elif status == OrderStatus.DELIVERED:
        event_dict = {"event_type": "order_delivered", **status_update_dict}
        await produce_message("order_delivered", event_dict, producer)
    elif status == OrderStatus.RETURNED:
        event_dict = {"event_type": "order_returned", **status_update_dict}
        await produce_message("order_returned", event_dict, producer)
    elif status == OrderStatus.CANCELLED:
        event_dict = {"event_type": "order_cancelled", **status_update_dict}
        await produce_message("order_cancelled", event_dict, producer)

    return db_order
