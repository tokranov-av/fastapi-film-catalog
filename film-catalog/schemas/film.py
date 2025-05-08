from pydantic import BaseModel


class FilmBase(BaseModel):
    """Базовая модель фильма."""

    id: int
    name: str
    description: str
    production_year: int
    country: str
    genre: str


class Film(FilmBase):
    """Модель фильма."""
