from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Annotated
from app.models.product_models import ProductCategory, ProductColor, ProductCreate, ProductSize, ProductUpdate, Product
from app.models.product_models import Color
from app.models.product_models import Size
from app.db.db_connection import DB_SESSION
from app.utils import is_category_exists
from app.kafka.producer import produce_message, KAFKA_PRODUCER
import json
app = FastAPI() 


router = APIRouter()

async def product_add(product: ProductCreate, session: DB_SESSION, producer: KAFKA_PRODUCER = KAFKA_PRODUCER):
    try:
        # Check if categories exist
        for category_id in product.product_category_ids:
            if not is_category_exists(category_id):
                raise HTTPException(status_code=404, detail=f"Category with id {category_id} not found")
        
        # Create the product
        db_product = Product(
            product_name=product.product_name,
            product_description=product.product_description,
            product_price=product.product_price,
            product_image_url=product.product_image_url
        )
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        
        # Add product categories
        if product.product_category_ids:
            for category_id in product.product_category_ids:
                db_product_category = ProductCategory(product_id=db_product.product_id, category_id=category_id)
                session.add(db_product_category)
        
        # Add sizes and product_sizes
        for size in product.sizes:
            db_size = Size(size_name=size.size_name)
            session.add(db_size)
            session.commit()
            session.refresh(db_size)

            product_size = ProductSize(product_id=db_product.product_id, size_id=db_size.size_id)
            session.add(product_size)
        
        # Add colors and product_colors
        for color in product.colors:
            db_color = Color(color_name=color.color_name)
            session.add(db_color)
            session.commit()
            session.refresh(db_color)

            product_color = ProductColor(product_id=db_product.product_id, color_id=db_color.color_id)
            session.add(product_color)

        # Produce Kafka message with color_id and size_id
        product_dict = {
            "product_id": db_product.product_id,
            "product_name": db_product.product_name,
            "product_description": db_product.product_description,
            "product_price": db_product.product_price,
            "product_image_url": db_product.product_image_url,
            "product_category_ids": product.product_category_ids,
            "colors": [
                {
                    "color_id": product_color.color_id,
                    "color_name": product_color.color.color_name
                } for product_color in db_product.colors
            ],
            "sizes": [
                {
                    "size_id": product_size.size_id,
                    "size_name": product_size.size.size_name
                } for product_size in db_product.sizes
            ],
            "message": "product added successfully",
            "event_type": "product_creation"
        }
        
        await produce_message("product_creation", product_dict, producer)
        
        session.commit()
    
    except Exception as e:
        session.rollback()  # Rollback changes on exception
        raise e
    
    finally:
        session.close()  # Close the session

    return {"message": "product added successfully"}



async def read_product_by_id(product_id: int, session: DB_SESSION):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


async def read_products_by_name(name: str, session: DB_SESSION):
    db_statement = select(Product).where(Product.product_name == name)
    product = session.exec(db_statement).all()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


async def read_products_by_category(category: str, session: DB_SESSION):
    db_statement = select(Product).where(Product.product_category == category)
    products = session.exec(db_statement).all()
    if not products:
        raise HTTPException(
            status_code=404, detail="No Product found in this category")
    return products


async def read_products(session: DB_SESSION):
    products = session.exec(select(Product)).all()
    return products

async def read_products_with_pagination(session: DB_SESSION, offset: int = 0, limit: int = 10):
    products = session.exec(select(Product).offset(offset).limit(limit)).all()
    return products


async def update_product_by_id(product_id: int, product_update: ProductUpdate, session: DB_SESSION, producer: KAFKA_PRODUCER):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="product not found")

    try:
        # Update fields only if provided in product_update
        for field, value in product_update.dict().items():
            if value is not None:
                setattr(db_product, field, value)
        
        # Commit the changes to the database
        session.commit()
        session.refresh(db_product)

        # Producing product_updation_event after database commit
        product_updated_dict = product_update.model_dump()
        message_dict = {"product_id": product_id, **product_updated_dict, "event_type": "product_updation"}
        await produce_message("product_updation", message_dict, producer)

    except Exception as e:
        session.rollback()  # Rollback changes on exception
        raise e
    return db_product



async def delete_product_by_id(
    product_id: int,
    session: DB_SESSION,
    producer: KAFKA_PRODUCER = KAFKA_PRODUCER
):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Delete the product
    session.delete(db_product)
    session.commit()

    # Produce a Kafka event for product deletion
    message = {
        "product_id": product_id,
        "message": "Product deleted successfully",
        "event_type": "product_deletion"
    }
    await produce_message("product_deletion", message, producer)

    return {"message": "Product deleted successfully"}


app.include_router(router)
