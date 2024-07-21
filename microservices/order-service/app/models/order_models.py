from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import Enum as SQLAEnum
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    RETURNED = "returned"
    CANCELLED = "cancelled"

class PaymentMethod(str, Enum):
    PAY_FAST = "pay_fast"  # Added for local payments
    STRIPE = "stripe"      # Added for international payments

class OrderCreate(SQLModel):
    user_id: int
    order_date: datetime
    shipping_address: str
    order_items: List["OrderItemCreate"]
    payment_method: PaymentMethod

    class Config:
        arbitrary_types_allowed = True

class OrderItemCreate(BaseModel):
    product_id: int
    color_id: int
    size_id: int
    quantity: int
    price_per_unit: float

    class Config:
        arbitrary_types_allowed = True

class Order(SQLModel, table=True):
    order_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    order_date: datetime
    shipping_address: str
    total_amount: float = Field(default=0)
    order_status: OrderStatus = Field(default=OrderStatus.PENDING, sa_column=SQLAEnum(OrderStatus))
    payment_method: PaymentMethod
    order_items: List["OrderItem"] = Relationship(
        back_populates="order", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    class Config:
        arbitrary_types_allowed = True

class OrderItem(SQLModel, table=True):
    order_item_id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.order_id")
    product_id: int
    color_id: int
    size_id: int
    quantity: int
    price_per_unit: float
    order: Order = Relationship(back_populates="order_items")

    class Config:
        arbitrary_types_allowed = True

class OrderUpdate(SQLModel):
    shipping_address: Optional[str] = None
    order_status: Optional[OrderStatus] = None

    class Config:
        arbitrary_types_allowed = True
