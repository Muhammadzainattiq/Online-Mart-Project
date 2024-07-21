from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.handlers.product_crud import (
    product_add,
    read_product_by_id,
    read_products_by_name,
    read_products_by_category,
    read_products,
    read_products_with_pagination,
    update_product_by_id,
    delete_product_by_id
)
from app.models.product_models import ProductCreate, ProductUpdate
from app.db.db_connection import get_session

product_router = APIRouter(prefix="/product")


@product_router.post('/add_product')
async def create_product(added_product: Annotated[ProductCreate, Depends(product_add)]):
    return added_product

@product_router.get('/read_product_by_id/{product_id}')
async def get_product_by_id(product: Annotated[ProductCreate, Depends(read_product_by_id)]):
    return product


@product_router.get('/read_products_by_name/{name}')
async def get_products_by_name(product: Annotated[ProductCreate, Depends(read_products_by_name)]):
    return product

@product_router.get('/read_products_by_category/{category}')
async def get_products_by_category(product: Annotated[ProductCreate, Depends(read_products_by_category)]):
    return product

@product_router.get('/read_all_products')
async def read_all_products(products: Annotated[List[ProductCreate], Depends(read_products,
)]):
    return products

@product_router.get('/read_all_products_with_pagination')
async def read_all_products_with_pagination(products: Annotated[List[ProductCreate], Depends(read_products_with_pagination
)], offset: int = 0, limit: int = 10):
    return products

@product_router.delete('/delete_product/{product_id}')
async def delete_product(message:Annotated[ProductCreate, Depends(delete_product_by_id)]):
    return message

@product_router.put('/update_product/{product_id}')
async def update_product(updated_product:Annotated[ProductCreate, Depends(update_product_by_id)]):
    return updated_product

