import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.film_catalog_urls.crud import storage
from main import app
from schemas.film import Film
from testing.utils import create_film


@pytest.fixture(
    params=[
        "some-slug",
        pytest.param("slg", id="min_length_slug"),
        pytest.param("qwerty-foo-bar-baz-z", id="max_length_slug"),
    ],
)
def film(request: SubRequest) -> Film:
    return create_film(slug=request.param)


def test_delete(
    client_with_token: TestClient,
    film: Film,
) -> None:
    assert storage.exists(film.slug)

    url = app.url_path_for("delete_film", slug=film.slug)
    response = client_with_token.delete(url=url)

    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
    assert not storage.exists(film.slug)
