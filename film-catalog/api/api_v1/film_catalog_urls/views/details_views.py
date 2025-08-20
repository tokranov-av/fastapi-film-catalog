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

MovieBySlug = Annotated[
    Movie,
    Depends(prefetch_film),
]


@router.get(
    path="/",
    response_model=MovieRead,
)
def read_movie(
    movie: MovieBySlug,
) -> Movie:
    return movie


@router.put(
    path="/",
    response_model=MovieRead,
)
def update_movie(
    movie: MovieBySlug,
    movie_in: MovieUpdate,
) -> Movie:
    return storage.update(
        movie=movie,
        movie_in=movie_in,
    )


@router.patch(
    path="/",
    response_model=MovieRead,
)
def update_movie_partial(
    movie: MovieBySlug,
    movie_in: MoviePartialUpdate,
) -> Movie:
    return storage.update_partial(
        movie=movie,
        movie_in=movie_in,
    )


@router.delete(
    path="/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(
    movie: MovieBySlug,
) -> None:
    storage.delete(movie=movie)


@router.post(
    path="/transfer/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def transfer_movie(slug: str) -> None:
    raise NotImplementedError
