from fastapi import APIRouter

from .film_catalog_urls.views import router as film_catalog_urls

router = APIRouter(
    prefix="/v1",
)

router.include_router(film_catalog_urls)
