from starlette.config import Config
from datetime import timedelta
try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL")

SECRET_KEY = config.get("SECRET_KEY")
ALGORITHM = config.get("ALGORITHM")


ADMIN_EMAIL = config.get("ADMIN_EMAIL")
ADMIN_PASSWORD = config.get("ADMIN_PASSWORD")


KAFKA_BOOTSTRAP_SERVER = config.get("KAFKA_BOOTSTRAP_SERVER")
KONG_ADMIN_URL = config.get("KONG_ADMIN_URL")