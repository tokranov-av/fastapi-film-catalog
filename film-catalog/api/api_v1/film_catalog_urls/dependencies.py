from fastapi import HTTPException
from starlette import status

from schemas.film import Film

from .crud import FILMS


def prefetch_film(movie_id: int) -> Film:
    film: Film | None = next(
        (film for film in FILMS if film.id == movie_id),
        None,
    )

    if film:
        return film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with id = {movie_id} not found",
    )
