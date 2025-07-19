from datetime import datetime
from typing import Any

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from core.config import TIME_ZONE
from main import app
from schemas.film import (
    Film,
    FilmCreate,
)
from testing.utils import build_film_create_random_slug, get_random_string


def test_create_film(client_with_token: TestClient) -> None:
    url = app.url_path_for("create_film")
    film_create = FilmCreate(
        name=get_random_string(),
        description=get_random_string(),
        production_year=datetime.now(tz=TIME_ZONE).year,
        country=get_random_string(),
        genre=get_random_string(),
        slug=get_random_string(),
    ).model_dump()

    response = client_with_token.post(url=url, json=film_create)

    assert response.status_code == status.HTTP_201_CREATED, response.text

    response_data = response.json()

    assert response_data == film_create, response_data


def test_create_film_already_exists(client_with_token: TestClient, film: Film) -> None:
    url = app.url_path_for("create_film")

    response = client_with_token.post(url=url, json=film.model_dump())

    assert response.status_code == status.HTTP_409_CONFLICT, response.text

    expected_message = f"Film with slug = {film.slug!r} already exists."
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
    def film_create_values(
        self,
        request: SubRequest,
    ) -> tuple[dict[str, Any], str]:
        film_create = build_film_create_random_slug()
        data = film_create.model_dump(mode="json")
        slug, err_type = request.param
        data["slug"] = slug

        return data, err_type

    def test_invalid_slug(
        self,
        client_with_token: TestClient,
        film_create_values: tuple[dict[str, Any], str],
    ) -> None:
        url = app.url_path_for("create_film")
        create_data, expected_error_type = film_create_values

        response = client_with_token.post(
            url=url,
            json=create_data,
        )

        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text

        error_detail = response.json()["detail"][0]

        assert error_detail["type"] == expected_error_type, error_detail
