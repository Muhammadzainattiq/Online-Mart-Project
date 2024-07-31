from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL")

KAFKA_BOOTSTRAP_SERVER = config("KAFKA_BOOTSTRAP_SERVER")

SENDER_EMAIL = config("SENDER_EMAIL")

EMAIL_PASSWORD = config("EMAIL_PASSWORD")
