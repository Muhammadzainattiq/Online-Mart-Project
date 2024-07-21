from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.handlers.category_crud import (
    category_add,
    update_category_by_id,
    delete_category_by_id
)
from app.models.product_models import Category
from app.db.db_connection import get_session

category_router = APIRouter(prefix="/category")


@category_router.post('/add_category')
async def create_category(added_category: Annotated[Category, Depends(category_add)]):
    return added_category


@category_router.delete('/delete_category/{category_id}')
async def delete_category(message:Annotated[Category, Depends(delete_category_by_id)]):
    return message

@category_router.put('/update_category/{category_id}')
async def update_category(updated_category:Annotated[Category, Depends(update_category_by_id)]):
    return updated_category
