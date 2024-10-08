from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field, BigInteger
from pydantic import EmailStr

# Models for User and Authentication

class LoginModel(SQLModel):
    user_email: EmailStr
    user_password: str

class SignUpModel(LoginModel):
    user_name: str
    phone_number: str = Field(max_length=15)
    user_address: str = Field(max_length=70)

class UserModel(SignUpModel):
    pass

class User(UserModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    payment_details: Optional["PaymentDetails"] = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})

class UserUpdate(SQLModel):
    user_name: Optional[str] = None
    phone_number: Optional[str] = None
    user_email: Optional[EmailStr] = None
    user_password: Optional[str] = None


# New Model for Payment Details

class PaymentDetailsCreate(SQLModel):
    card_number: str = Field(max_length=16)
    card_expiry: str = Field(max_length=5)
    card_cvc: str = Field(max_length=3)

class PaymentDetails(PaymentDetailsCreate, table=True):
    payment_details_id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    user: "User" = Relationship(back_populates="payment_details")
