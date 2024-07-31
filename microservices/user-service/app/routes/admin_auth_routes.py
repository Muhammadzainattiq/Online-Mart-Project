from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.handlers.admin_auth import admin_signup_fn, admin_login_fn, admin_get
from app.models.admin_models import AdminModel

admin_auth_router = APIRouter(prefix="/admin_auth")

@admin_auth_router.post('/signup_admin')
async def signup_admin(admin_data: Annotated[AdminModel, Depends(admin_signup_fn)]):
    if admin_data:
        return {"message": "You are successfully registered"}
    else:
        raise HTTPException(status_code=401, detail="Admin registration failed")
        
        
@admin_auth_router.post('/login_admin')
async def login_admin(admin_data: Annotated[AdminModel, Depends(admin_login_fn)]):
    if admin_data:
        return {"message": "You are successfully logged in"}
    else:
        raise HTTPException(status_code=401, detail="Admin login failed")

@admin_auth_router.get('/get_admin', response_model=AdminModel)
async def get_admin(admin: Annotated[AdminModel, Depends(admin_get)]):
    if admin:
        return admin
    else:
        raise HTTPException(status_code=401, detail="Admin not found")
