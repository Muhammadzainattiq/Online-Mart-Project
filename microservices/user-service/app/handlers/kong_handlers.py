from fastapi import HTTPException, logger
import httpx
from app.settings import KONG_ADMIN_URL

async def create_kong_consumer(consumer_id: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{KONG_ADMIN_URL}/consumers/",
                json={"username": consumer_id}
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        logger.error(f"Failed to create Kong consumer: {exc.response.text}")
        raise HTTPException(status_code=exc.response.status_code, detail="Failed to create Kong consumer")

async def create_jwt_credentials(consumer_id: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{KONG_ADMIN_URL}/consumers/{consumer_id}/jwt",
                json={}
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        logger.error(f"Failed to create JWT credentials: {exc.response.text}")
        raise HTTPException(status_code=exc.response.status_code, detail="Failed to create JWT credentials")

async def get_kong_jwt_token(consumer_id: str, jwt_secret: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{KONG_ADMIN_URL}/consumers/{consumer_id}/jwt",
                headers={"Authorization": f"Bearer {jwt_secret}"}
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        logger.error(f"Failed to get Kong JWT token: {exc.response.text}")
        raise HTTPException(status_code=exc.response.status_code, detail="Failed to get Kong JWT token")