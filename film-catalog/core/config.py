import logging
from os import getenv
from zoneinfo import ZoneInfo

LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

REDIS_HOST = "localhost"
REDIS_PORT = int(getenv("REDIS_PORT", "0")) or 6379

REDIS_DB = 0
REDIS_DB_TOKENS = 1
REDIS_DB_USERS = 2
REDIS_DB_MOVIES = 3

REDIS_TOKENS_SET_NAME = "tokens"
REDIS_MOVIES_HASH_NAME = "movies"

TIME_ZONE = ZoneInfo("Europe/Moscow")
