from fastapi import HTTPException
from starlette import status

from schemas.film import Film
from .crud import FILMS


def prefetch_film(slug: str) -> Film:
    film: Film | None = next(
        (film for film in FILMS if film.slug == slug),
        None,
    )

    if film:
        return film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with slug = {slug} not found",
    )
