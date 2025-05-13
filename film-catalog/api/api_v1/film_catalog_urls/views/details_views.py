from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from api.api_v1.film_catalog_urls.crud import storage
from api.api_v1.film_catalog_urls.dependencies import prefetch_film
from schemas.film import Film


router = APIRouter(
    prefix="/slug",
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


@router.get(
    path="/",
)
def read_movie_description(
    film: Annotated[
        Film,
        Depends(prefetch_film),
    ],
) -> Film:
    return film


@router.delete(
    path="/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_film(
    film: Annotated[
        Film,
        Depends(prefetch_film),
    ],
) -> None:
    storage.delete(film=film)
