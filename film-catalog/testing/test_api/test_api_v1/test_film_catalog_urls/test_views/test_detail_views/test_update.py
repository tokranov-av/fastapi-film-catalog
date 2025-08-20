from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.film_catalog_urls.crud import storage
from main import app
from schemas.film import Movie, MovieUpdate
from testing.utils import create_movie_random_slug


@pytest.mark.apitest
class TestUpdate:
    @pytest.fixture
    def movie(self, request: SubRequest) -> Generator[Movie]:
        name, description = request.param
        movie = create_movie_random_slug(
            name=name,
            description=description,
        )
        yield movie
        storage.delete_by_slug(movie.slug)

    @pytest.mark.apitest
    @pytest.mark.parametrize(
        "movie, updated_data",
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
        indirect=["movie"],
    )
    def test_update_movie_details(
        self,
        client_with_token: TestClient,
        movie: Movie,
        updated_data: dict[str, str | int],
    ) -> None:
        url = app.url_path_for(
            "update_movie",
            slug=movie.slug,
        )
        movie_data = MovieUpdate(**movie.model_dump()).model_dump()

        response = client_with_token.put(
            url,
            json=movie_data | updated_data,
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        movie_db = storage.get_by_slug(slug=movie.slug)
        assert movie_db
        for key, value in updated_data.items():
            assert getattr(movie_db, key) == value
