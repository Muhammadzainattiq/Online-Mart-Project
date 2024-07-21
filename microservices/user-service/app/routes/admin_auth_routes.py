from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlmodel import Session
from app.handlers.admin_auth import (admin_signup_fn, admin_login_fn, admin_get)
from app.models.admin_models import AdminModel
from app.db.db_connection import get_session

admin_auth_router = APIRouter(prefix="/admin_auth")


@admin_auth_router.post('/signup_admin')
async def signup_admin(response:Response, tokens_data: Annotated[AdminModel, Depends(admin_signup_fn)]):
    if tokens_data:
        print("tokens_data: ", tokens_data)
        response.set_cookie(key="access_token", value=tokens_data["access_token"]["token"], expires=tokens_data["access_token"]["expiry_time"])

        response.set_cookie(key="refresh_token", value = tokens_data["refresh_token"]["token"], expires= tokens_data["refresh_token"]["expiry_time"])
        return "You are sucessfully registered"
    else:
        raise HTTPException(status_code=401, detail="Admin registration failed")
        
        
@admin_auth_router.post('/login_admin')
async def login_admin(response:Response, request:Request, tokens_data: Annotated[AdminModel, Depends(admin_login_fn)]):
    if tokens_data:
        print("tokens_data: ", tokens_data)
        print("request.headers", request.headers)

        response.set_cookie(key="access_token", value=tokens_data["access_token"]["token"], expires=tokens_data["access_token"]["expiry_time"])

        response.set_cookie(key="refresh_token", value = tokens_data["refresh_token"]["token"], expires= tokens_data["refresh_token"]["expiry_time"])


        return "You are sucessfully logged in"

    else:
        raise HTTPException(status_code=401, detail="Admin login failed")

@admin_auth_router.get('/get_admin', response_model=AdminModel)
async def get_admin(admin: Annotated[AdminModel, Depends(admin_get)]):
    if admin:
        return admin
    else:
        raise HTTPException(status_code=401, detail="Admin not found")