from enum import Enum
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    RETURNED = "returned"


class PaymentMethod(str, Enum):
    STRIPE = "stripe"
    PAYFAST = "pay_fast"


class PaymentCreate(SQLModel):
    order_id: int
    user_id: int
    amount: float
    method: PaymentMethod


class Payment(PaymentCreate, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: PaymentStatus = Field(default=PaymentStatus.PENDING)
    transaction_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PaymentUser(SQLModel, table=True):
    user_id: int = Field(primary_key=True)
    card_number: str
    card_cvc: str
    card_expiry: str

