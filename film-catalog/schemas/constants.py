__all__ = (
    "MAX_LENGTH_FOR_DESCRIPTION",
    "MAX_YEAR",
    "MIN_LENGTH_STRING",
    "MIN_YEAR",
)

from datetime import datetime

from core.config import TIME_ZONE

MAX_LENGTH_FOR_DESCRIPTION: int = 1000
MIN_LENGTH_STRING: int = 3
MIN_YEAR: int = 1900
MAX_YEAR: int = datetime.now(tz=TIME_ZONE).year + 10
