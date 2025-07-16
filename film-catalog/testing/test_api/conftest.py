from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from api.api_v1.auth.services import redis_tokens
from api.api_v1.film_catalog_urls.crud import storage
from main import app
from schemas.film import Film
from testing.utils import create_film


@pytest.fixture
def client() -> Generator[TestClient]:
    with TestClient(app=app) as client:
        yield client


@pytest.fixture(scope="module")
def auth_token() -> Generator[str]:
    token = redis_tokens.generate_and_save_token()
    yield token
    redis_tokens.delete_token(token)


@pytest.fixture(scope="module")
def client_with_token(auth_token: str) -> Generator[TestClient]:
    headers = {"Authorization": f"Bearer {auth_token}"}
    with TestClient(app=app, headers=headers) as client:
        yield client


@pytest.fixture
def film() -> Generator[Film]:
    film = create_film()
    yield film
    storage.delete(film)
