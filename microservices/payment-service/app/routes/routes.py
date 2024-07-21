from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.crud_user import (
    user_add,
    read_user_by_id,
    read_user_by_email,
    read_all_users,
    update_user_by_id,
    delete_user_by_id
)
from app.user_models import UserModel, UserUpdate
from app.db_connection import get_session

router = APIRouter()


@router.post('/add_user')
async def create_user(added_user: Annotated[UserModel, Depends(user_add)]):
    return added_user

@router.get('/users/{user_id}')
async def get_user_by_id(user: Annotated[UserModel, Depends(read_user_by_id)]):
    return user


@router.get('/users/email/{email}')
async def get_user_by_email(user: Annotated[UserModel, Depends(read_user_by_email)]):
    return user

@router.get('/users')
async def read_all_users(users: Annotated[List[UserModel], Depends(read_all_users)]):
    return users

@router.delete('/users/delete_user/{user_id}')
async def delete_user(message:Annotated[UserModel, Depends(delete_user_by_id)]):
    return message

@router.put('/users/update_user/{user_id}')
async def update_user(updated_user:Annotated[UserModel, Depends(update_user_by_id)]):
    return updated_user

