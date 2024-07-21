from enum import Enum
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"

class PaymentCreate(SQLModel):
    order_id: int
    user_id: int
    amount: float
    method: PaymentMethod

class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id", unique=True)
    user_id: int
    amount: float
    status: PaymentStatus = Field(default=PaymentStatus.PENDING)
    method: PaymentMethod
    transaction_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    order: "Order" = Relationship(back_populates="payment")

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    total_amount: float
    status: str
    payment: Optional[Payment] = Relationship(back_populates="order")
