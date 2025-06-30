import logging

LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

REDIS_HOST = "localhost"
REDIS_PORT = 6379

REDIS_DB = 0
REDIS_DB_TOKENS = 1
REDIS_DB_USERS = 2
REDIS_DB_FILMS = 3

REDIS_TOKENS_SET_NAME = "tokens"
REDIS_FILMS_HASH_NAME = "films"
