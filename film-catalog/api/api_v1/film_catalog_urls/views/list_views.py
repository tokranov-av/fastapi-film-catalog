from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from api.api_v1.film_catalog_urls.crud import (
    MovieAlreadyExistsError,
    storage,
)
from api.api_v1.film_catalog_urls.dependencies import (
    api_token_or_user_basic_auth_required_for_unsafe_methods,
)
from schemas.film import (
    Movie,
    MovieCreate,
    MovieRead,
)

router = APIRouter(
    prefix="/films",
    tags=["Films"],
    dependencies=[
        Depends(api_token_or_user_basic_auth_required_for_unsafe_methods),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only for unsafe methods.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API token",
                    },
                },
            },
        },
    },
)


@router.get(
    path="/",
    response_model=list[MovieRead],
)
def get_list_of_movies() -> list[Movie]:
    return storage.get()


@router.post(
    path="/",
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Movie with such slug already exists.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie with slug = 'name' already exists.",
                    },
                },
            },
        },
    },
)
def create_movie(
    movie_create: MovieCreate,
) -> Movie:
    try:
        return storage.create_or_raise_if_exists(movie_create)
    except MovieAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Movie with slug = {movie_create.slug!r} already exists.",
        ) from None
