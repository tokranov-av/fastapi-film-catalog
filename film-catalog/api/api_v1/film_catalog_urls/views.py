from datetime import datetime
import random
from typing import Annotated

from annotated_types import MinLen, Gt, Lt

from fastapi import (
    Depends,
    APIRouter,
    Form,
    status,
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


@router.post(
    path="/",
    response_model=Film,
    status_code=status.HTTP_201_CREATED,
)
def create_film(
    name: Annotated[str, MinLen(1), Form()],
    description: Annotated[str, Form()],
    production_year: Annotated[int, Gt(1900), Lt(datetime.now().year + 1), Form()],
    country: Annotated[str, MinLen(3), Form()],
    genre: Annotated[str, MinLen(1), Form()],
):
    return Film(
        id=random.randint(1, 1000),
        name=name,
        description=description,
        production_year=production_year,
        country=country,
        genre=genre,
    )


@router.get(path="/{movie_id}/")
def read_movie_description(
    film: Annotated[
        Film,
        Depends(prefetch_film),
    ],
):
    return film
