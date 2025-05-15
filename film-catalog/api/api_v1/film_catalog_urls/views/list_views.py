from fastapi import (
    APIRouter,
    status,
)

from schemas.film import (
    Film,
    FilmCreate,
    FilmRead,
)
from api.api_v1.film_catalog_urls.crud import storage

router = APIRouter(
    prefix="/films",
    tags=["Films"],
)


@router.get(
    path="/",
    response_model=list[FilmRead],
)
def get_list_of_films() -> list[Film]:
    return storage.get()


@router.post(
    path="/",
    response_model=FilmRead,
    status_code=status.HTTP_201_CREATED,
)
def create_film(film_create: FilmCreate) -> Film:
    return storage.create(film_create)
