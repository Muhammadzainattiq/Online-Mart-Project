from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlmodel import Session
from app.handlers.user_auth import (signup_fn, login_fn, user_get)
from app.models.user_models import UserModel, UserUpdate
from app.db.db_connection import get_session

user_auth_router = APIRouter(prefix="/user_auth")


@user_auth_router.post('/signup_user/')
async def signup_user(response:Response, tokens_data: Annotated[dict, Depends(signup_fn)]):
    if tokens_data:
        print("tokens_data: ", tokens_data)
        response.set_cookie(key="access_token", value=tokens_data["access_token"]["token"], expires=tokens_data["access_token"]["expiry_time"])

        response.set_cookie(key="refresh_token", value = tokens_data["refresh_token"]["token"], expires= tokens_data["refresh_token"]["expiry_time"])
        return "You are sucessfully registered"
    else:
        raise HTTPException(status_code=401, detail="User registration failed")
        
        
@user_auth_router.post('/login_user/')
async def login_user(response:Response, request:Request, tokens_data: Annotated[UserModel, Depends(login_fn)]):
    if tokens_data:
        print("tokens_data: ", tokens_data)
        print("request.headers", request.headers)

        response.set_cookie(key="access_token", value=tokens_data["access_token"]["token"], expires=tokens_data["access_token"]["expiry_time"])

        response.set_cookie(key="refresh_token", value = tokens_data["refresh_token"]["token"], expires= tokens_data["refresh_token"]["expiry_time"])


        return "You are sucessfully logged in"

    else:
        raise HTTPException(status_code=401, detail="User login failed")

@user_auth_router.get('/get_user/', response_model=UserModel)
async def get_user(user: Annotated[UserModel, Depends(user_get)]):
    if user:
        return user
    else:
        raise HTTPException(status_code=401, detail="User not found")