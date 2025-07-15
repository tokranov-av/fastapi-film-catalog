from datetime import datetime

from fastapi import status
from fastapi.testclient import TestClient

from core.config import TIME_ZONE
from main import app
from schemas.film import FilmCreate
from testing.utils import get_random_string


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
