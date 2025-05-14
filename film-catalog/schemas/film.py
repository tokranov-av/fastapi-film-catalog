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
StringManLen1000 = Annotated[str, MaxLen(1000)]


class FilmBase(BaseModel):
    """Базовая модель информации о фильме."""

    name: StringMinLen1
    description: StringManLen1000
    production_year: Annotated[int, Gt(1900), Lt(datetime.now().year + 1)]
    country: StringMinLen3
    genre: StringMinLen1


class FilmCreate(FilmBase):
    """Модель для создания информации о фильме."""

    slug: StringMinLen1


class FilmUpdate(FilmBase):
    """Модель для обновления информации о фильме."""


class FilmPartialUpdate(FilmBase):
    """Модель для частичного обновления информации о фильме."""

    name: StringMinLen1 | None = None
    description: StringManLen1000 | None = None
    production_year: Annotated[int, Gt(1900), Lt(datetime.now().year + 1)] | None = None
    country: StringMinLen3 | None = None
    genre: StringMinLen1 | None = None


class Film(FilmBase):
    """Модель информации о фильме."""

    slug: str
