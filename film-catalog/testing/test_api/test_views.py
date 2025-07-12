from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app=app)


def test_root_view() -> None:
    # TODO: fake data
    name = "John"
    query = {"name": name}
    expected_message = f"Hello, {name}!"

    response = client.get("/", params=query)

    response_data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert response_data["message"] == expected_message, response_data
