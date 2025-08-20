from datetime import datetime
from typing import Any

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from core.config import TIME_ZONE
from main import app
from schemas.film import (
    Movie,
    MovieCreate,
)
from testing.utils import build_movie_create_random_slug, get_random_string

pytestmark = pytest.mark.apitest


@pytest.mark.apitest
def test_create_movie(client_with_token: TestClient) -> None:
    url = app.url_path_for("create_movie")
    movie_create = MovieCreate(
        name=get_random_string(),
        description=get_random_string(),
        production_year=datetime.now(tz=TIME_ZONE).year,
        country=get_random_string(),
        genre=get_random_string(),
        slug=get_random_string(),
    ).model_dump()

    response = client_with_token.post(url=url, json=movie_create)

    assert response.status_code == status.HTTP_201_CREATED, response.text

    response_data = response.json()

    assert response_data == movie_create, response_data


@pytest.mark.apitest
def test_create_movie_already_exists(
    client_with_token: TestClient,
    movie: Movie,
) -> None:
    url = app.url_path_for("create_movie")

    response = client_with_token.post(url=url, json=movie.model_dump())

    assert response.status_code == status.HTTP_409_CONFLICT, response.text

    expected_message = f"Movie with slug = {movie.slug!r} already exists."
    response_data = response.json()

    assert response_data["detail"] == expected_message, response.text


class TestCreateInvalid:
    @pytest.fixture(
        params=[
            pytest.param(("sl", "string_too_short"), id="too-short-slug"),
            pytest.param(
                ("zaqwsx-foo-bar-baz-z10", "string_too_long"),
                id="too-long-slug",
            ),
        ],
    )
    def movie_create_values(
        self,
        request: SubRequest,
    ) -> tuple[dict[str, Any], str]:
        movie_create = build_movie_create_random_slug()
        data = movie_create.model_dump(mode="json")
        slug, err_type = request.param
        data["slug"] = slug

        return data, err_type

    @pytest.mark.apitest
    def test_invalid_slug(
        self,
        client_with_token: TestClient,
        movie_create_values: tuple[dict[str, Any], str],
    ) -> None:
        url = app.url_path_for("create_movie")
        create_data, expected_error_type = movie_create_values

        response = client_with_token.post(
            url=url,
            json=create_data,
        )

        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text

        error_detail = response.json()["detail"][0]

        assert error_detail["type"] == expected_error_type, error_detail
