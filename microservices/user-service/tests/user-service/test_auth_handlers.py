import pytest
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.handlers.auth_handlers import decode_token, password_hashing, verify_password, TokenDecodingError
from app.settings import ALGORITHM, SECRET_KEY

### Test for `decode_token`

@pytest.mark.asyncio
async def test_decode_token_valid():
    # Step 1: Generate a valid token
    payload = {"user_email": "test@example.com", "exp": datetime.utcnow() + timedelta(minutes=15)}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    # Step 2: Decode the token
    decoded_token = await decode_token(token)
    
    # Step 3: Verify the decoded token
    assert decoded_token["user_email"] == "test@example.com"
    assert "exp" in decoded_token


@pytest.mark.asyncio
async def test_decode_token_invalid():
    # Step 1: Provide an invalid token
    invalid_token = "invalidtoken"

    # Step 2: Attempt to decode the token and catch the exception
    with pytest.raises(TokenDecodingError):
        await decode_token(invalid_token)


### Test for `password_hashing`

@pytest.mark.asyncio
async def test_password_hashing():
    # Step 1: Hash a plain-text password
    password = "mypassword"
    hashed_password = await password_hashing(password)
    
    # Step 2: Verify that the hashed password is not the same as the plain-text password
    assert hashed_password != password
    assert hashed_password is not None
    assert isinstance(hashed_password, str)


### Test for `verify_password`

@pytest.mark.asyncio
async def test_verify_password_correct():
    # Step 1: Hash a plain-text password
    password = "mypassword"
    hashed_password = await password_hashing(password)
    
    # Step 2: Verify the hashed password with the correct plain-text password
    is_verified = await verify_password(hashed_password, password)
    
    # Step 3: Ensure the password verification is successful
    assert is_verified is True


@pytest.mark.asyncio
async def test_verify_password_incorrect():
    # Step 1: Hash a plain-text password
    password = "mypassword"
    hashed_password = await password_hashing(password)
    
    # Step 2: Attempt to verify the hashed password with an incorrect plain-text password
    is_verified = await verify_password(hashed_password, "wrongpassword")
    
    # Step 3: Ensure the password verification fails
    assert is_verified is False
