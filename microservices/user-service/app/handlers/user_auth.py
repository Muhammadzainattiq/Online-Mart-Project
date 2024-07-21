from typing import Annotated
from sqlmodel import Session, select
from fastapi import Depends, HTTPException
from app.db.db_connection import get_session
from app.handlers.auth_handlers import verify_password
from app.settings import ACCESS_EXPIRY_TIME, REFRESH_EXPIRY_TIME
from app.models.user_models import (User, UserToken, SignUpModel, LoginModel)
from app.handlers.auth_handlers import password_hashing, verify_password, generate_token, decode_token
from fastapi.security import OAuth2PasswordBearer
from app.kafka.producer import KAFKA_PRODUCER, produce_message
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login_user")

DB_SESSION = Annotated[Session, Depends(get_session)]

async def signup_fn(user_form: SignUpModel, session: DB_SESSION, producer: KAFKA_PRODUCER):
    user = session.exec(select(User).where(
        User.user_email == user_form.user_email)).first()
    if user:
        raise HTTPException(status_code=409, detail="User Already Exists. Please try signing in.")
    
    hashed_password = await password_hashing(user_form.user_password)
    user_form.user_password = hashed_password
    
    print("User Form", user_form)
    
    user = User(**user_form.model_dump())
    
    session.add(user)
    session.commit()
    session.refresh(user)  # Ensure user_id is populated
    
    # Produce the event after user is committed and refreshed
    user_dict = user.model_dump()
    event_dict = {"event_type": "user_creation", **user_dict}
    await produce_message("user_creation", event_dict, producer)
    
    data = {
        "user_name": user.user_name,
        "user_email": user.user_email
    }
    
    access_token = await generate_token(data=data, expiry_time=ACCESS_EXPIRY_TIME)
    refresh_token = await generate_token(data=data, expiry_time=REFRESH_EXPIRY_TIME)
    
    access_expiry_time = ACCESS_EXPIRY_TIME.total_seconds()
    refresh_expiry_time = REFRESH_EXPIRY_TIME.total_seconds()
    
    token = UserToken(user_id=user.user_id, refresh_token=refresh_token)
    session.add(token)
    session.commit()
    session.refresh(token)
    
    return {
        "access_token": {
            "token": access_token,
            "expiry_time": access_expiry_time
        },
        "refresh_token": {
            "token": refresh_token,
            "expiry_time": refresh_expiry_time
        }
    }


async def login_fn(login_form: LoginModel, session: DB_SESSION):
    statement = select(User).where(User.user_email == login_form.user_email)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    elif not verify_password(user.user_password, login_form.user_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    else:
        data = {
            "user_name": user.user_name,
            "user_email": user.user_email
        }
        access_token = await generate_token(data=data, expiry_time=ACCESS_EXPIRY_TIME)
        refresh_token = await generate_token(data=data, expiry_time=REFRESH_EXPIRY_TIME)
        
        access_expiry_time = ACCESS_EXPIRY_TIME.total_seconds()
        refresh_expiry_time = REFRESH_EXPIRY_TIME.total_seconds()

        to_update_token = session.exec(
            select(UserToken).where(UserToken.user_id == user.user_id)).one()
        to_update_token.refresh_token = refresh_token
        session.add(to_update_token)
        session.commit()
        session.refresh(to_update_token)
        return {"access_token": {
        "token": access_token,
        "expiry_time": access_expiry_time
        },
        "refresh_token": {
        "token": refresh_token,
        "expiry_time": refresh_expiry_time
        }
    }



def user_get(token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[Session, Depends(get_session)]):
    try:
        if token:
            data = decode_token(token)
            user_email = data["user_email"]
            user = session.exec(select(User).where(
                User.user_email == user_email)).first()
            return user

    except:
        raise HTTPException(status_code=404, detail="Token not found")
