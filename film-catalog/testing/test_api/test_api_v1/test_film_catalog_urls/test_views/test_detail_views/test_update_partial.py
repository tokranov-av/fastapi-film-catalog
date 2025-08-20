from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.film_catalog_urls.crud import storage
from main import app
from schemas import MAX_LENGTH_FOR_DESCRIPTION
from schemas.film import Movie
from testing.utils import create_movie_random_slug


class TestUpdatePartial:
    @pytest.fixture
    def movie(self, request: SubRequest) -> Generator[Movie]:
        movie = create_movie_random_slug(description=request.param)
        yield movie
        storage.delete_by_slug(movie.slug)

    @pytest.mark.apitest
    @pytest.mark.parametrize(
        "movie, new_description",
        [
            pytest.param(
                "some description",
                "",
                id="some-description-to-no-description",
            ),
            pytest.param(
                "",
                "some-description",
                id="no-description-to-some-description",
            ),
            pytest.param(
                "a" * MAX_LENGTH_FOR_DESCRIPTION,
                "",
                id="max-description-to-min-description",
            ),
            pytest.param(
                "",
                "a" * MAX_LENGTH_FOR_DESCRIPTION,
                id="min-description-to-max-description",
            ),
        ],
        indirect=["movie"],
    )
    def test_update_film_partial(
        self,
        client_with_token: TestClient,
        movie: Movie,
        new_description: str,
    ) -> None:
        url = app.url_path_for(
            "update_movie_partial",
            slug=movie.slug,
        )

        response = client_with_token.patch(
            url,
            json={"description": new_description},
        )

        assert response.status_code == status.HTTP_200_OK, response.text

        movie_db = storage.get_by_slug(slug=movie.slug)

        assert movie_db
        assert movie_db.description == new_description
