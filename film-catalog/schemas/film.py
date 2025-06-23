from datetime import datetime
from typing import Annotated

from annotated_types import (
    MaxLen,
    MinLen,
    Gt,
    Lt,
)
from pydantic import BaseModel

StringMinLen1 = Annotated[str, MinLen(1)]
StringMinLen3 = Annotated[str, MinLen(3)]
StringMaxLen1000 = Annotated[str, MaxLen(1000)]
IntegerGt1900LtNow = Annotated[int, Gt(1900), Lt(datetime.now().year + 1)]


class FilmBase(BaseModel):
    """Базовая модель информации о фильме."""

    name: StringMinLen1
    description: StringMaxLen1000
    production_year: IntegerGt1900LtNow
    country: StringMinLen3
    genre: StringMinLen1


class FilmCreate(FilmBase):
    """Модель для создания информации о фильме."""

    slug: StringMinLen1


class FilmUpdate(FilmBase):
    """Модель для обновления информации о фильме."""


class FilmPartialUpdate(BaseModel):
    """Модель для частичного обновления информации о фильме."""

    name: StringMinLen1 | None = None
    description: StringMaxLen1000 | None = None
    production_year: IntegerGt1900LtNow | None = None
    country: StringMinLen3 | None = None
    genre: StringMinLen1 | None = None


class FilmRead(FilmBase):
    """Модель для чтения информации о фильме."""

    slug: str


class Film(FilmBase):
    """Модель информации о фильме."""

    slug: str
    notes: str = ""
