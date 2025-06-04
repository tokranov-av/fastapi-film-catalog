import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FILMS_STORAGE_FILEPATH = BASE_DIR / "films.json"

LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

# Only for demo!
# no real users in code!
USERS_DB: dict[str, str] = {
    # username: password
    "vinni": "password",
    "ia": "qwerty",
}

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_DB_TOKENS = 1

REDIS_TOKENS_SET_NAME = "tokens"
