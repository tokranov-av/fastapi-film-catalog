from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.film_catalog_urls.crud import storage
from main import app
from schemas.film import Movie, MovieUpdate
from testing.utils import create_film_random_slug


@pytest.mark.apitest
class TestUpdate:
    @pytest.fixture
    def film(self, request: SubRequest) -> Generator[Movie]:
        name, description = request.param
        film = create_film_random_slug(
            name=name,
            description=description,
        )
        yield film
        storage.delete_by_slug(film.slug)

    @pytest.mark.apitest
    @pytest.mark.parametrize(
        "film, updated_data",
        [
            pytest.param(
                (
                    "Some name",
                    "Some description",
                ),
                {"name": "New name"},
                id="update-name",
            ),
            pytest.param(
                (
                    "Some name",
                    "Some description",
                ),
                {"description": "New description"},
                id="update-description",
            ),
            pytest.param(
                (
                    "Some name",
                    "Some description",
                ),
                {"production_year": 2021},
                id="update-production-year",
            ),
            pytest.param(
                (
                    "Some name",
                    "Some description",
                ),
                {"country": "New country"},
                id="update-country",
            ),
        ],
        indirect=["film"],
    )
    def test_update_film_details(
        self,
        client_with_token: TestClient,
        film: Movie,
        updated_data: dict[str, str | int],
    ) -> None:
        url = app.url_path_for(
            "update_film",
            slug=film.slug,
        )
        film_data = MovieUpdate(**film.model_dump()).model_dump()

        response = client_with_token.put(
            url,
            json=film_data | updated_data,
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        film_db = storage.get_by_slug(slug=film.slug)
        assert film_db
        for key, value in updated_data.items():
            assert getattr(film_db, key) == value
