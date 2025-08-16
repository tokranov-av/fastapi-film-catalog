from typing import (
    Annotated,
)

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from api.api_v1.film_catalog_urls.crud import (
    storage,
)
from api.api_v1.film_catalog_urls.dependencies import (
    prefetch_film,
)
from schemas.film import (
    Movie,
    MoviePartialUpdate,
    MovieRead,
    MovieUpdate,
)

router = APIRouter(
    prefix="/{slug}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Movie not found",
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

FilmBySlug = Annotated[
    Movie,
    Depends(prefetch_film),
]


@router.get(
    path="/",
    response_model=MovieRead,
)
def read_film(
    film: FilmBySlug,
) -> Movie:
    return film


@router.put(
    path="/",
    response_model=MovieRead,
)
def update_film(
    film: FilmBySlug,
    film_in: MovieUpdate,
) -> Movie:
    return storage.update(
        film=film,
        film_in=film_in,
    )


@router.patch(
    path="/",
    response_model=MovieRead,
)
def update_film_partial(
    film: FilmBySlug,
    film_in: MoviePartialUpdate,
) -> Movie:
    return storage.update_partial(
        film=film,
        film_in=film_in,
    )


@router.delete(
    path="/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_film(
    film: FilmBySlug,
) -> None:
    storage.delete(film=film)


@router.post(
    path="/transfer/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def transfer_movie(slug: str) -> None:
    raise NotImplementedError
