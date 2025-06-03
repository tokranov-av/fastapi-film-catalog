from fastapi import (
    APIRouter,
    Depends,
    status,
)

from api.api_v1.film_catalog_urls.dependencies import (
    save_storage_state,
    api_token_or_user_basic_auth_required_for_unsafe_methods,
)
from schemas.film import (
    Film,
    FilmCreate,
    FilmRead,
)
from api.api_v1.film_catalog_urls.crud import (
    storage,
)

router = APIRouter(
    prefix="/films",
    tags=["Films"],
    dependencies=[
        Depends(save_storage_state),
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
        }
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
)
def create_film(
    film_create: FilmCreate,
) -> Film:
    return storage.create(film_create)
