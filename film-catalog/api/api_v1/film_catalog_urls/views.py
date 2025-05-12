from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
    status,
)

from schemas.film import (
    Film,
    FilmCreate,
)
from .dependencies import prefetch_film
from .crud import storage

router = APIRouter(
    prefix="/films",
    tags=["Films"],
)


@router.get(
    path="/",
    response_model=list[Film],
)
def get_list_of_films() -> list[Film]:
    return storage.get()


@router.post(
    path="/",
    response_model=Film,
    status_code=status.HTTP_201_CREATED,
)
def create_film(film_create: FilmCreate) -> Film:
    return storage.create(film_create)


@router.get(
    path="/{slug}/",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Film not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie with 'slug' not found",
                    },
                },
            },
        },
    },
)
def read_movie_description(
    film: Annotated[
        Film,
        Depends(prefetch_film),
    ],
) -> Film:
    return film


@router.delete(
    path="/{slug}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Film not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie with 'slug' not found",
                    },
                },
            },
        },
    },
)
def delete_film(
    film: Annotated[
        Film,
        Depends(prefetch_film),
    ],
) -> None:
    storage.delete(film=film)
