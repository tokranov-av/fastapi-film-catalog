import random
import string
from datetime import datetime
from unittest import TestCase

from api.api_v1.film_catalog_urls.crud import storage
from core.config import TIME_ZONE
from schemas.film import (
    Film,
    FilmCreate,
    FilmPartialUpdate,
    FilmUpdate,
)


class FilmStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.film = self.create_film()
        self.expected_description = "Another description"
        self.expected_genre = "Another genre"

    def tearDown(self) -> None:
        storage.delete(self.film)

    @classmethod
    def create_film(cls) -> Film:
        film_create = FilmCreate(
            name="Some name",
            description="Some description",
            production_year=datetime.now(tz=TIME_ZONE).year,
            country="Some country",
            genre="Some genre",
            slug="".join(
                random.choices(  # noqa: S311
                    string.ascii_letters,
                    k=8,
                ),
            ),
        )

        return storage.create(film_create)

    def test_update(self) -> None:
        film_update = FilmUpdate(**self.film.model_dump())
        film_update.description = self.expected_description
        film_update.genre = self.expected_genre

        updated_film = storage.update(
            film=self.film,
            film_in=film_update,
        )

        self.assertEqual(self.expected_description, updated_film.description)
        self.assertEqual(self.expected_genre, updated_film.genre)

    def test_partial_update(self) -> None:
        film_partial_update = FilmPartialUpdate(
            description=self.expected_description,
            genre=self.expected_genre,
        )
        expected_name = self.film.name

        partial_updated_film = storage.update_partial(
            film=self.film,
            film_in=film_partial_update,
        )

        self.assertEqual(self.expected_description, partial_updated_film.description)
        self.assertEqual(self.expected_genre, partial_updated_film.genre)
        self.assertEqual(expected_name, partial_updated_film.name)
