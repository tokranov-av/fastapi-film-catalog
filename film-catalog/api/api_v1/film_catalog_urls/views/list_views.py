from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from api.api_v1.film_catalog_urls.crud import (
    FilmAlreadyExistsError,
    storage,
)
from api.api_v1.film_catalog_urls.dependencies import (
    api_token_or_user_basic_auth_required_for_unsafe_methods,
)
from schemas.film import (
    Film,
    FilmCreate,
    FilmRead,
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
    response_model=list[FilmRead],
)
def get_list_of_films() -> list[Film]:
    return storage.get()


@router.post(
    path="/",
    response_model=FilmRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Film with such slug already exists.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Film with slug = 'name' already exists.",
                    },
                },
            },
        },
    },
)
def create_film(
    film_create: FilmCreate,
) -> Film:
    try:
        return storage.create_or_raise_if_exists(film_create)
    except FilmAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Film with slug = {film_create.slug!r} already exists.",
        ) from None
