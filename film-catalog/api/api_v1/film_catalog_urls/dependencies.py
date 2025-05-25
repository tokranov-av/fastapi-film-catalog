import logging
from typing import (
    Annotated,
)

from fastapi import (
    Query,
    Request,
    BackgroundTasks,
    HTTPException,
    status,
)

from core.config import (
    API_TOKENS,
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


def api_token_required(
    request: Request,
    api_token: Annotated[
        str,
        Query(),
    ] = "",
):
    """Проверяет наличие в запросе корректного токена."""
    if request.method in UNSAFE_METHODS and api_token not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API token",
        )
    yield
