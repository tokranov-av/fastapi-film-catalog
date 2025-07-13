import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app=app)


def test_root_view() -> None:
    expected_message = "Hello, World!"

    response = client.get("/")

    response_data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert response_data["message"] == expected_message, response_data


@pytest.mark.parametrize(
    "name",
    [
        # TODO: fake data
        "John",
        "",
        "John Smith",
        "!$#%&",
    ],
)
def test_root_view_custom_name(name: str) -> None:
    query = {"name": name}
    expected_message = f"Hello, {name}!"

    response = client.get("/", params=query)

    response_data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert response_data["message"] == expected_message, response_data
