import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.film_catalog_urls.crud import storage
from main import app
from schemas.film import Movie
from testing.utils import create_movie


@pytest.fixture(
    params=[
        "some-slug",
        pytest.param("slg", id="min_length_slug"),
        pytest.param("qwerty-foo-bar-baz-z", id="max_length_slug"),
    ],
)
def movie(request: SubRequest) -> Movie:
    return create_movie(slug=request.param)


@pytest.mark.apitest
def test_delete(
    client_with_token: TestClient,
    movie: Movie,
) -> None:
    assert storage.exists(movie.slug)

    url = app.url_path_for("delete_movie", slug=movie.slug)
    response = client_with_token.delete(url=url)

    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
    assert not storage.exists(movie.slug)
