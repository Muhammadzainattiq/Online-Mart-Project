from starlette.config import Config
from datetime import timedelta
try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL")


ACCESS_EXPIRY_TIME = timedelta(minutes = int(config.get("ACCESS_EXPIRY_TIME")))
REFRESH_EXPIRY_TIME = timedelta(hours = int(config.get("REFRESH_EXPIRY_TIME")))

ADMIN_ACCESS_EXPIRY_TIME = timedelta(minutes = int(config.get("ADMIN_ACCESS_EXPIRY_TIME")))
ADMIN_REFRESH_EXPIRY_TIME = timedelta(hours = int(config.get("ADMIN_REFRESH_EXPIRY_TIME")))

SECRET_KEY = config.get("SECRET_KEY")
ALGORITHM = config.get("ALGORITHM")


ADMIN_EMAIL = config.get("ADMIN_EMAIL")
ADMIN_PASSWORD = config.get("ADMIN_PASSWORD")


KAFKA_BOOTSTRAP_SERVER = config.get("KAFKA_BOOTSTRAP_SERVER")