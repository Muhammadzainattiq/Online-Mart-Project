from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
from app.handlers.user_auth import signup_fn, login_fn, user_get
from app.models.user_models import UserModel

user_auth_router = APIRouter(prefix="/user_auth")

@user_auth_router.post('/signup_user/')
async def signup_user(user_data: Annotated[dict, Depends(signup_fn)]):
    if user_data:
        return {"message": "You are successfully registered"}
    else:
        raise HTTPException(status_code=401, detail="User registration failed")
        
        
@user_auth_router.post('/login_user/')
async def login_user(user_data: Annotated[dict, Depends(login_fn)]):
    if user_data:
        return {"message": "You are successfully logged in"}
    else:
        raise HTTPException(status_code=401, detail="User login failed")

@user_auth_router.get('/get_user/', response_model=UserModel)
async def get_user(user: Annotated[UserModel, Depends(user_get)]):
    if user:
        return user
    else:
        raise HTTPException(status_code=401, detail="User not found")
