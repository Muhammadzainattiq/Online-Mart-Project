from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Enum as SQLAEnum
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, UTC
from enum import Enum


class Notification(SQLModel, table=True):
    notification_id: int | None= Field(default=None, primary_key=True)
    user_id: int
    message: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class NotificationCreate(SQLModel):
    user_id: int
    message: str



class NotificationUser(SQLModel, table = True):
    user_id: int = Field(default= None, primary_key=True)
    user_name: str
    user_email: str