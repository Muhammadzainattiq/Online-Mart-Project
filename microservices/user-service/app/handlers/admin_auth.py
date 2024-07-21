from typing import Annotated
from sqlmodel import Session, select
from fastapi import Depends, HTTPException
from app.db.db_connection import get_session
from app.handlers.auth_handlers import verify_password
from app.settings import ADMIN_ACCESS_EXPIRY_TIME, ADMIN_REFRESH_EXPIRY_TIME
from app.models.admin_models import (Admin, AdminToken, AdminSignUpModel, AdminLoginModel)
from app.handlers.auth_handlers import password_hashing, verify_password, generate_token, decode_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

DB_SESSION = Annotated[Session, Depends(get_session)]

async def admin_signup_fn(admin_form: AdminSignUpModel, session: DB_SESSION):
    admin = session.exec(select(Admin).where(
        Admin.admin_email == admin_form.admin_email)).first()
    if admin:
        raise HTTPException(status_code=409, detail="Admin Already Exists. Please try signing in.")
    hashed_password = await password_hashing(admin_form.admin_password)
    admin_form.admin_password = hashed_password
    admin = Admin(**admin_form.model_dump())
    session.add(admin)
    session.commit()
    session.refresh(admin)
    data = {
        "admin_name": admin.admin_name,
        "admin_email": admin.admin_email
    }
    access_token = await generate_token(data=data, expiry_time=ADMIN_ACCESS_EXPIRY_TIME)
    refresh_token = await generate_token(data=data, expiry_time=ADMIN_REFRESH_EXPIRY_TIME)

    access_expiry_time = ADMIN_ACCESS_EXPIRY_TIME.total_seconds()
    refresh_expiry_time = ADMIN_REFRESH_EXPIRY_TIME.total_seconds()

    token = AdminToken(admin_id=admin.admin_id, refresh_token=refresh_token)
    session.add(token)
    session.commit()
    session.refresh(token)
    return {"access_token": {
        "token": access_token,
        "expiry_time": access_expiry_time
        },
        "refresh_token": {
        "token": refresh_token,
        "expiry_time": refresh_expiry_time
        }
    }


async def admin_login_fn(login_form: AdminLoginModel, session: DB_SESSION):
    statement = select(Admin).where(Admin.admin_email == login_form.admin_email)
    admin = session.exec(statement).first()

    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    elif not verify_password(admin.admin_password, login_form.admin_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    else:
        data = {
            "admin_name": admin.admin_name,
            "admin_email": admin.admin_email
        }
        access_token = await generate_token(data=data, expiry_time=ADMIN_ACCESS_EXPIRY_TIME)
        refresh_token = await generate_token(data=data, expiry_time=ADMIN_REFRESH_EXPIRY_TIME)
        
        access_expiry_time = ADMIN_ACCESS_EXPIRY_TIME.total_seconds()
        refresh_expiry_time = ADMIN_REFRESH_EXPIRY_TIME.total_seconds()

        to_update_token = session.exec(
            select(AdminToken).where(Admin.admin_id == admin.admin_id)).one()
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



def admin_get(token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[Session, Depends(get_session)]):
    try:
        if token:
            data = decode_token(token)
            admin_email = data["admin_email"]
            admin = session.exec(select(Admin).where(
                Admin.admin_email == admin_email)).first()
            return admin

    except:
        raise HTTPException(status_code=404, detail="Token not found")
