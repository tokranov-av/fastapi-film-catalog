__all__ = (
    "build_film_create",
    "build_film_create_random_slug",
    "create_film",
    "create_film_random_slug",
    "get_random_string",
)

import random
import string
from datetime import datetime

from api.api_v1.film_catalog_urls.crud import storage
from core.config import TIME_ZONE
from schemas.film import Movie, MovieCreate


def get_random_string(length: int = 8) -> str:
    """Возвращает случайную строку из букв ascii_letters заданной длины."""
    return "".join(
        random.choices(  # noqa: S311
            string.ascii_letters,
            k=length,
        ),
    )


def build_film_create(
    slug: str,
    name: str | None = None,
    description: str | None = None,
) -> MovieCreate:
    return MovieCreate(
        name=name if name is not None else get_random_string(),
        description=description if description is not None else get_random_string(),
        production_year=datetime.now(tz=TIME_ZONE).year,
        country=get_random_string(),
        genre=get_random_string(),
        slug=slug,
    )


def build_film_create_random_slug(
    name: str | None = None,
    description: str | None = None,
) -> MovieCreate:
    return build_film_create(
        slug=get_random_string(),
        name=name,
        description=description,
    )


def create_film(
    slug: str,
    name: str | None = None,
    description: str | None = None,
) -> Movie:
    """Создает и сохраняет фильм в хранилище."""
    film_create = build_film_create(
        slug=slug,
        name=name,
        description=description,
    )

    return storage.create(film_create)


def create_film_random_slug(
    name: str | None = None,
    description: str | None = None,
) -> Movie:
    film_create = build_film_create_random_slug(
        name=name,
        description=description,
    )

    return storage.create(film_create)
