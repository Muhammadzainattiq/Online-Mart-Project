from typing import Annotated
from sqlmodel import Session, select
from fastapi import Depends, HTTPException
import httpx
import os
import logging
from app.db.db_connection import get_session
from app.handlers.auth_handlers import verify_password
from app.models.admin_models import Admin, AdminSignUpModel, AdminLoginModel
from app.handlers.auth_handlers import password_hashing, verify_password, decode_token
from fastapi.security import OAuth2PasswordBearer
from app.kafka.producer import KAFKA_PRODUCER, produce_message

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login_user")

KONG_ADMIN_URL = os.getenv("KONG_ADMIN_URL")
logger = logging.getLogger(__name__)
from app.handlers.kong_handlers import create_kong_consumer, create_jwt_credentials, get_kong_jwt_token




async def admin_signup_fn(admin_form: AdminSignUpModel, session: Annotated[Session, Depends(get_session)]):
    admin = session.exec(select(Admin).where(Admin.admin_email == admin_form.admin_email)).first()
    if admin:
        raise HTTPException(status_code=409, detail="Admin Already Exists. Please try signing in.")
    
    hashed_password = await password_hashing(admin_form.admin_password)
    admin_form.admin_password = hashed_password
    admin = Admin(**admin_form.model_dump())
    session.add(admin)
    session.commit()
    session.refresh(admin)
    
    kong_consumer = await create_kong_consumer(admin.admin_email)
    jwt_credentials = await create_jwt_credentials(admin.admin_email)
    
    return {"message": "Admin created successfully, please login to receive tokens"}

async def admin_login_fn(login_form: AdminLoginModel, session: Annotated[Session, Depends(get_session)]):
    statement = select(Admin).where(Admin.admin_email == login_form.admin_email)
    admin = session.exec(statement).first()

    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    elif not verify_password(admin.admin_password, login_form.admin_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    jwt_credentials = await create_jwt_credentials(admin.admin_email)
    kong_token = await get_kong_jwt_token(admin.admin_email, jwt_credentials["secret"])

    return {"token": kong_token}


def admin_get(token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[Session, Depends(get_session)]):
    try:
        if token:
            data = decode_token(token)
            admin_email = data["admin_email"]
            admin = session.exec(select(Admin).where(Admin.admin_email == admin_email)).first()
            return admin
    except Exception as e:
        logger.error(f"Failed to decode token: {str(e)}")
        raise HTTPException(status_code=404, detail="Token not found")
