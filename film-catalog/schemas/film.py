from datetime import datetime
from typing import Annotated

from annotated_types import (
    Gt,
    Lt,
    MaxLen,
    MinLen,
)
from pydantic import BaseModel

from core.config import TIME_ZONE

StringMinLen3 = Annotated[str, MinLen(3)]
StringMaxLen1000 = Annotated[str, MaxLen(1000)]
IntegerGt1900LtNow = Annotated[
    int,
    Gt(1900),
    Lt(datetime.now(tz=TIME_ZONE).year + 10),
]


class FilmBase(BaseModel):
    """Базовая модель информации о фильме."""

    name: StringMinLen3
    description: StringMaxLen1000
    production_year: IntegerGt1900LtNow
    country: StringMinLen3
    genre: StringMinLen3


class FilmCreate(FilmBase):
    """Модель для создания информации о фильме."""

    slug: Annotated[str, MinLen(3), MaxLen(20)]


class FilmUpdate(FilmBase):
    """Модель для обновления информации о фильме."""


class FilmPartialUpdate(BaseModel):
    """Модель для частичного обновления информации о фильме."""

    name: StringMinLen3 | None = None
    description: StringMaxLen1000 | None = None
    production_year: IntegerGt1900LtNow | None = None
    country: StringMinLen3 | None = None
    genre: StringMinLen3 | None = None


class FilmRead(FilmBase):
    """Модель для чтения информации о фильме."""

    slug: str


class Film(FilmBase):
    """Модель информации о фильме."""

    slug: str
    notes: str = ""
