from datetime import datetime
from unittest import TestCase

from core.config import TIME_ZONE
from schemas.film import Film, FilmCreate, FilmUpdate


class FilmSchemesTestCase(TestCase):
    def setUp(self) -> None:
        self.some_notes = "some-notes"
        self.film = Film(
            name="Some name",
            description="Some description",
            production_year=datetime.now(tz=TIME_ZONE).year,
            country="Россия",
            genre="Семейный",
            slug="some-slug",
            notes=self.some_notes,
        )

    def test_film_create(self) -> None:
        """Проверка создания экземпляра фильма."""
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
            notes=self.some_notes,
        )

        self.assertEqual(film_create.name, film.name)
        self.assertEqual(film_create.description, film.description)
        self.assertEqual(film_create.production_year, film.production_year)
        self.assertEqual(film_create.country, film.country)
        self.assertEqual(film_create.genre, film.genre)
        self.assertEqual(film_create.slug, film.slug)
        self.assertEqual(self.some_notes, film.notes)

    def test_film_update(self) -> None:
        """Проверка обновления экземпляра фильма."""
        film_update = FilmUpdate(
            name="Movie title",
            description="Movie description",
            production_year=datetime.now(tz=TIME_ZONE).year - 1,
            country="США",
            genre="Мелодрама",
        )

        for field_name, value in film_update:
            if hasattr(self.film, field_name):
                setattr(self.film, field_name, value)

        self.assertEqual(self.film.name, film_update.name)
        self.assertEqual(self.film.description, film_update.description)
        self.assertEqual(self.film.production_year, film_update.production_year)
        self.assertEqual(self.film.country, film_update.country)
        self.assertEqual(self.film.genre, film_update.genre)
