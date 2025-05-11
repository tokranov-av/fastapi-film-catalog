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


@router.get(path="/{slug}/")
def read_movie_description(
    film: Annotated[
        Film,
        Depends(prefetch_film),
    ],
) -> Film:
    return film
