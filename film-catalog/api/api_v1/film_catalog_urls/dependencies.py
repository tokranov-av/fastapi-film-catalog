from fastapi import HTTPException
from starlette import status

from schemas.film import Film
from .crud import storage


def prefetch_film(slug: str) -> Film:
    film: Film | None = storage.get_by_slug(slug=slug)

    if film:
        return film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with {slug} not found",
    )
