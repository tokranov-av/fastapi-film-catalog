from datetime import datetime
from unittest import TestCase

from core.config import TIME_ZONE
from schemas.film import Film, FilmCreate


class FilmCreateTestCase(TestCase):
    def test_film_create(self) -> None:
        some_notes = "some-notes"
        film_create = FilmCreate(
            name="Some name",
            description="Some description",
            production_year=datetime.now(tz=TIME_ZONE).year,
            country="Россия",
            genre="Семейный",
            slug="some-slug",
        )

        film = Film(
            **film_create.model_dump(),
            notes=some_notes,
        )

        self.assertEqual(film_create.name, film.name)
        self.assertEqual(film_create.description, film.description)
        self.assertEqual(film_create.production_year, film.production_year)
        self.assertEqual(film_create.country, film.country)
        self.assertEqual(film_create.genre, film.genre)
        self.assertEqual(film_create.slug, film.slug)
        self.assertEqual(some_notes, film.notes)
