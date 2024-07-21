from app.db.db_connection import engine
from sqlmodel import Session, select
from app.models.product_models import Category
def is_category_exists(category_id:int):
    with Session(engine) as session:
        check = session.exec(statement=select(Category).where(Category.category_id == category_id)).all()

    if check:
        return True
    else:
        return False
    

def get_category_name(category_id:int):
    with Session(engine) as session:
        category = session.exec(statement=select(Category).where(Category.category_id == category_id)).first()
        return category.name

