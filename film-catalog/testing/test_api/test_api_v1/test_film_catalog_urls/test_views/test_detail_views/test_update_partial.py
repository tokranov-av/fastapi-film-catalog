from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.film_catalog_urls.crud import storage
from main import app
from schemas import MAX_LENGTH_FOR_DESCRIPTION
from schemas.film import Film
from testing.utils import create_film


class TestUpdatePartial:
    @pytest.fixture
    def film(self, request: SubRequest) -> Generator[Film]:
        slug, description = request.param
        yield create_film(
            slug=slug,
            description=description,
        )
        storage.delete_by_slug(slug)

    @pytest.mark.parametrize(
        "film, new_description",
        [
            pytest.param(
                ("foo", "some description"),
                "",
                id="some-description-to-no-description",
            ),
            pytest.param(
                ("bar", ""),
                "some-description",
                id="no-description-to-some-description",
            ),
            pytest.param(
                ("max-to-min", "a" * MAX_LENGTH_FOR_DESCRIPTION),
                "",
                id="max-description-to-min-description",
            ),
            pytest.param(
                ("min-to-max", ""),
                "a" * MAX_LENGTH_FOR_DESCRIPTION,
                id="min-description-to-max-description",
            ),
        ],
        indirect=["film"],
    )
    def test_update_film_partial(
        self,
        client_with_token: TestClient,
        film: Film,
        new_description: str,
    ) -> None:
        url = app.url_path_for(
            "update_film_partial",
            slug=film.slug,
        )

        response = client_with_token.patch(
            url,
            json={"description": new_description},
        )

        assert response.status_code == status.HTTP_200_OK, response.text

        film_db = storage.get_by_slug(slug=film.slug)

        assert film_db
        assert film_db.description == new_description
