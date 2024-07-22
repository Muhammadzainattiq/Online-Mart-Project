from sqlmodel import Session
from app.db.db_connection import engine
from app.models.user_models import User
from fastapi import HTTPException

async def get_user_name_from_id(user_id: int):
    with Session(engine) as session:
        try:
            user_details = session.get(User, user_id)
            if user_details:
                return user_details.user_name
            else:
                raise HTTPException(status_code=404, detail="User not found")
        except:
            raise HTTPException(status_code=404, detail="User not found")