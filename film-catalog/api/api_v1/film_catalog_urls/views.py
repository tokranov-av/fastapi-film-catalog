from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
)

from schemas.film import Film

from .dependencies import prefetch_film
from .crud import FILMS

router = APIRouter(
    prefix="/films",
    tags=["Films"],
)


@router.get(
    path="/",
    response_model=list[Film],
)
def get_list_of_films():
    return FILMS


@router.get(path="/{movie_id}/")
def read_movie_description(
    film: Annotated[
        Film,
        Depends(prefetch_film),
    ],
):
    return film
