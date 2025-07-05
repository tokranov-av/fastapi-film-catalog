from datetime import datetime
from unittest import TestCase

from pydantic import ValidationError

from core.config import TIME_ZONE
from schemas.film import (
    Film,
    FilmCreate,
    FilmPartialUpdate,
    FilmUpdate,
)


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

    def test_partial_update(self) -> None:
        """Проверка частичного обновления экземпляра фильма."""
        partial_updates = [
            ("field name: name", FilmPartialUpdate(name="Movie title")),
            (
                "field name: description",
                FilmPartialUpdate(description="Movie description"),
            ),
            ("field name: production_year", FilmPartialUpdate(production_year=2025)),
            ("field name: country", FilmPartialUpdate(country="Country")),
            ("field name: genre", FilmPartialUpdate(genre="Genre")),
        ]

        for msg, partial_update in partial_updates:
            with self.subTest(msg=msg):
                for field_name, value in partial_update.model_dump(
                    exclude_unset=True,
                ).items():
                    if hasattr(self.film, field_name):
                        setattr(self.film, field_name, value)

                    self.assertEqual(
                        getattr(partial_update, field_name),
                        getattr(self.film, field_name),
                    )

    def test_partial_update_with_empty_instance(self) -> None:
        """Проверка частичного обновления экземпляра фильма с пустым экземпляром."""
        film_partial_update = FilmPartialUpdate()
        film = self.film.model_copy()

        for field_name, value in film_partial_update.model_dump(
            exclude_unset=True,
        ).items():
            if hasattr(self.film, field_name):
                setattr(self.film, field_name, value)

        self.assertEqual(film.name, self.film.name)
        self.assertEqual(film.description, self.film.description)
        self.assertEqual(film.production_year, self.film.production_year)
        self.assertEqual(film.country, self.film.country)
        self.assertEqual(film.genre, self.film.genre)

    def test_film_create_slug_too_short(self) -> None:
        """Проверяет выброс исключения при слишком коротком слаге."""
        with self.assertRaises(ValidationError) as exc_info:
            FilmCreate(
                name="sl",
                description="Some description",
                production_year=datetime.now(tz=TIME_ZONE).year,
                country="Россия",
                genre="Семейный",
                slug="some-slug",
            )

        error_details = exc_info.exception.errors()[0]
        expected_type = "string_too_short"
        self.assertEqual(
            expected_type,
            error_details["type"],
        )

    def test_film_create_slug_too_short_with_regex(self) -> None:
        with self.assertRaisesRegex(
            ValidationError,
            expected_regex="String should have at least 3 characters",
        ):
            FilmCreate(
                name="sl",
                description="Some description",
                production_year=datetime.now(tz=TIME_ZONE).year,
                country="Россия",
                genre="Семейный",
                slug="some-slug",
            )
