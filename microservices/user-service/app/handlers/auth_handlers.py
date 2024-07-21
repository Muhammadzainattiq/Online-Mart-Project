from jose import jwt,JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import json
from app.settings import ALGORITHM, SECRET_KEY
pwd_context = CryptContext(schemes="bcrypt")
class TokenGenerationError(Exception):
    pass

class TokenDecodingError(Exception):
    pass

#This function will be used to generate both the access token and the refresh token. when we want to generate the refresh token we will pass it the refresh token expiry time and when we want to generate the access token, we will pass it the access token expiry time.

async def generate_token(data: dict, expiry_time: timedelta):
    try:
        to_encode_data = data.copy()
        expire = datetime.now(timezone.utc) + expiry_time
        to_encode_data.update({"exp": expire.timestamp()})
        token = jwt.encode(to_encode_data, key=SECRET_KEY, algorithm=ALGORITHM)
        return token
    except JWTError as je:
        raise TokenGenerationError(f"JWT error occurred during token generation: {je}")


async def decode_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except JWTError as je:
        raise TokenDecodingError(f"JWT error occurred during token decoding: {je}")
    
    
async def password_hashing(password:str)->str:
    hashed_password = pwd_context.hash(password)
    return hashed_password

async def verify_password(hashed_password:str, password:str):
    is_password_verified = pwd_context.verify(password, hashed_password)
    return is_password_verified



