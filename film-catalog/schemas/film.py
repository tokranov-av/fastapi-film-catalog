from datetime import datetime
from typing import Annotated

from annotated_types import (
    MaxLen,
    MinLen,
    Gt,
    Lt,
)
from pydantic import BaseModel


class FilmBase(BaseModel):
    """Базовая модель фильма."""

    slug: str
    name: str
    description: str
    production_year: int
    country: str
    genre: str


class FilmCreate(FilmBase):
    """Модель для создания фильма."""

    slug: Annotated[str, MinLen(1)]
    name: Annotated[str, MinLen(1)]
    description: Annotated[str, MaxLen(1000)]
    production_year: Annotated[int, Gt(1900), Lt(datetime.now().year + 1)]
    country: Annotated[str, MinLen(3)]
    genre: Annotated[str, MinLen(1)]


class Film(FilmBase):
    """Модель фильма."""
