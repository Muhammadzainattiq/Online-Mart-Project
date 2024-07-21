from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Annotated
from app.user_models import User, UserModel, UserUpdate
from app.db_connection import get_session, DB_SESSION

app = FastAPI()


router = APIRouter()

async def user_add(user: UserModel, session: DB_SESSION):
    db_statement = select(User).where(User.user_email == user.user_email)
    db_user_info = session.exec(db_statement).first()

    if db_user_info:
        raise HTTPException(status_code=404, detail="User Already Exists (Try to Sign in.)")
    else:
        db_user = User(**user.dict())
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

async def read_user_by_id(user_id: int, session: DB_SESSION):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def read_user_by_email(email: str, session: DB_SESSION):
    db_statement = select(User).where(User.user_email == email)
    user = session.exec(db_statement).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
async def get_all_users(session: DB_SESSION):
    users = session.exec(select(User)).all()
    return users


async def read_all_users(session: DB_SESSION):
    users = await get_all_users(session)
    return users


async def update_user_by_id(user_id: int, user_update: UserUpdate, session: DB_SESSION):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user_update.dict().items():
        setattr(db_user, field, value)

    session.commit()
    session.refresh(db_user)
    return db_user


async def delete_user_by_id(user_id: int, session: DB_SESSION):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(db_user)
    session.commit()
    return {"message": "User deleted successfully"}



app.include_router(router)
