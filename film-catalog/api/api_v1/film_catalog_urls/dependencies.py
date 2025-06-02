import logging
from typing import (
    Annotated,
)

from fastapi import (
    Depends,
    Request,
    BackgroundTasks,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    HTTPBasic,
    HTTPBasicCredentials,
)

from core.config import (
    API_TOKENS,
    USERS_DB,
)
from schemas.film import (
    Film,
)
from .crud import (
    storage,
)

log = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)

static_api_token = HTTPBearer(
    scheme_name="Static API token",
    description="Your **Static API token** from the developer portal. [Read more](#)",
    auto_error=False,
)

user_basic_auth = HTTPBasic(
    scheme_name="Basic Auth",
    description="Basic username + password auth",
    auto_error=False,
)


def prefetch_film(slug: str) -> Film:
    film: Film | None = storage.get_by_slug(slug=slug)

    if film:
        return film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with slug '{slug}' not found",
    )


def save_storage_state(
    request: Request,
    background_tasks: BackgroundTasks,
):
    """Добавляет фоновую задачу сохранения описания о фильме в файл хранилище."""

    # Выполняется код до входа внутрь view функции
    yield
    # Выполняется код после покидания view функции
    if request.method in UNSAFE_METHODS:
        background_tasks.add_task(storage.save_state)
        log.debug(
            "Добавлена фоновая задача для сохранения описания о фильме в файл хранилище"
        )


def api_token_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
):
    """Проверяет наличие в запросе корректного токена."""
    if request.method not in UNSAFE_METHODS:
        return

    if api_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required",
        )

    if api_token.credentials not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
        )


def user_basic_auth_required_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return

    if (
        credentials
        and credentials.username in USERS_DB
        and USERS_DB[credentials.username] == credentials.password
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User credentials required. Invalid username or password.",
        headers={"WWW-Authenticate": "Basic"},
    )
