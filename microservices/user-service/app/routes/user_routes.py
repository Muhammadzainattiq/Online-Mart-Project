from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.handlers.user_crud import (
    read_user_by_id,
    read_user_by_email,
    read_all_users,
    update_user_by_id,
    delete_user_by_id
)
from app.models.user_models import UserModel, UserUpdate
from app.db.db_connection import get_session

user_router = APIRouter(prefix="/user")


@user_router.get('/get_user_by_id/{user_id}')
async def get_user_by_id(user: Annotated[UserModel, Depends(read_user_by_id)]):
    return user


@user_router.get('/get_user_by_email/{email}')
async def get_user_by_email(user: Annotated[UserModel, Depends(read_user_by_email)]):
    return user

@user_router.get('/get_all_users')
async def read_all_users(users: Annotated[List[UserModel], Depends(read_all_users)]):
    return users

@user_router.delete('/delete_user/{user_id}')
async def delete_user(message:Annotated[UserModel, Depends(delete_user_by_id)]):
    return message

@user_router.put('/update_user/{user_id}')
async def update_user(updated_user:Annotated[UserModel, Depends(update_user_by_id)]):
    return updated_user

