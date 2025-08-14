import os
from dotenv import load_dotenv
import pytz


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

REDIS_URL = os.getenv("REDIS_URL")

API_ENDPOINT = os.getenv("API_ENDPOINT")

BEARER_TOKEN = os.getenv("BEARER_TOKEN")

DELAY_DAYS_2 = 172800
DELAY_DAYS_1 = 86400
DELAY_HOUR_1 = 3600
DELAY_MINUTES_15 = 900
DELAY_MINUTES_5 = 300
DELAY_MINUTES_2 = 120


TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": os.getenv('DB_HOST'),
                "port": os.getenv('DB_PORT'),
                "user": os.getenv('DB_USER'),
                "password": os.getenv('DB_PASSWORD'),
                "database": os.getenv('DB_NAME'),
            },
        }
    },
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        }
    },
}
