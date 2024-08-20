from typing import Annotated
from sqlmodel import Session, select
from fastapi import Depends, HTTPException
import httpx
import os
import logging
from app.db.db_connection import get_session
from app.handlers.auth_handlers import verify_password
from app.models.user_models import User, SignUpModel, LoginModel
from app.handlers.auth_handlers import password_hashing, verify_password, decode_token
from fastapi.security import OAuth2PasswordBearer
from app.kafka.producer import KAFKA_PRODUCER, produce_message
from app.handlers.kong_handlers import create_kong_consumer, create_jwt_credentials, get_kong_jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login_user")
DB_SESSION = Annotated[Session, Depends(get_session)]

KONG_ADMIN_URL = os.getenv("KONG_ADMIN_URL", "http://localhost:8001")
logger = logging.getLogger(__name__)


async def signup_fn(user_form: SignUpModel, session: Annotated[Session, Depends(get_session)], producer: KAFKA_PRODUCER):
    user = session.exec(select(User).where(User.user_email == user_form.user_email)).first()
    if user:
        raise HTTPException(status_code=409, detail="User Already Exists. Please try signing in.")
    
    hashed_password = await password_hashing(user_form.user_password)
    user_form.user_password = hashed_password
    user = User(**user_form.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # kong_consumer = await create_kong_consumer(user.user_email)
    # jwt_credentials = await create_jwt_credentials(user.user_email)
    
    event_dict = {"event_type": "user_creation", **user.model_dump()}
    await produce_message("user_creation", event_dict, producer)
    
    return {"message": "User created successfully, please login to receive tokens"}

async def login_fn(login_form: LoginModel, session: Annotated[Session, Depends(get_session)]):
    statement = select(User).where(User.user_email == login_form.user_email)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    elif not verify_password(user.user_password, login_form.user_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    jwt_credentials = await create_jwt_credentials(user.user_email)
    kong_token = await get_kong_jwt_token(user.user_email, jwt_credentials["secret"])

    return {"token": kong_token}


def user_get(token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[Session, Depends(get_session)]):
    try:
        if token:
            data = decode_token(token)
            user_email = data["user_email"]
            user = session.exec(select(User).where(User.user_email == user_email)).first()
            return user
    except Exception as e:
        logger.error(f"Failed to decode token: {str(e)}")
        raise HTTPException(status_code=404, detail="Token not found")

