import logging

from fastapi import (
    BackgroundTasks,
    HTTPException,
)
from starlette import status

from schemas.film import Film
from .crud import storage

log = logging.getLogger(__name__)


def prefetch_film(slug: str) -> Film:
    film: Film | None = storage.get_by_slug(slug=slug)

    if film:
        return film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with {slug} not found",
    )


def save_storage_state(
    background_tasks: BackgroundTasks,
):
    log.info("First time inside dependency save_storage_state")
    yield
    background_tasks.add_task(storage.save_state)
    log.debug(
        "Добавлена фоновая задача для сохранения описания о фильме в файл хранилище"
    )
