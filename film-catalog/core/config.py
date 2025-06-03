import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FILMS_STORAGE_FILEPATH = BASE_DIR / "films.json"

LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

# Never store real tokens here!
# Only fake values.
API_TOKENS: frozenset[str] = frozenset(
    {
        "j5qMrWZ0UeFvF8LN9WlSSw",
        "gVWPhWAvNbduNKSE7MObew",
    }
)
# Only for demo!
# no real users in code!
USERS_DB: dict[str, str] = {
    # username: password
    "vinni": "password",
    "ia": "qwerty",
}
