
from fastapi import HTTPException
from sqlalchemy import select
from app.db.db_connection import DB_SESSION

from app.models.product_models import Category, CategoryUpdate, CategoryCreate

async def category_add(category:CategoryCreate, session:DB_SESSION):
    category_to_insert = Category.model_validate(category)
    session.add(category_to_insert)
    session.commit()
    session.refresh(category_to_insert)

    return category_to_insert


async def update_category_by_id(category_update: CategoryUpdate,category_id:int, session:DB_SESSION):
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="category not found")
    # Update fields only if provided in category_update
    for field, value in category_update.model_dump().items():
        if value is not None:  # Skip updating if value is None if you will miss this it will give an error message
            setattr(db_category, field, value)
    session.commit()
    session.refresh(db_category)
    return db_category


async def delete_category_by_id(category_id:int, session:DB_SESSION):
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="category not found")
    session.delete(db_category)
    session.commit()
    return {"message": "Category deleted successfully"}



