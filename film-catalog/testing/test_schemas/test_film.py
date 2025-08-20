from datetime import datetime
from unittest import TestCase

from pydantic import ValidationError

from core.config import TIME_ZONE
from schemas.film import (
    Movie,
    MovieCreate,
    MoviePartialUpdate,
    MovieUpdate,
)


class MovieSchemesTestCase(TestCase):
    def setUp(self) -> None:
        self.some_notes = "some-notes"
        self.movie = Movie(
            name="Some name",
            description="Some description",
            production_year=datetime.now(tz=TIME_ZONE).year,
            country="Россия",
            genre="Семейный",
            slug="some-slug",
            notes=self.some_notes,
        )

    def test_movie_create(self) -> None:
        """Проверка создания экземпляра фильма."""
        movie_create = MovieCreate(
            name="Some name",
            description="Some description",
            production_year=datetime.now(tz=TIME_ZONE).year,
            country="Россия",
            genre="Семейный",
            slug="some-slug",
        )

        movie = Movie(
            **movie_create.model_dump(),
            notes=self.some_notes,
        )

        self.assertEqual(movie_create.name, movie.name)
        self.assertEqual(movie_create.description, movie.description)
        self.assertEqual(movie_create.production_year, movie.production_year)
        self.assertEqual(movie_create.country, movie.country)
        self.assertEqual(movie_create.genre, movie.genre)
        self.assertEqual(movie_create.slug, movie.slug)
        self.assertEqual(self.some_notes, movie.notes)

    def test_movie_update(self) -> None:
        """Проверка обновления экземпляра фильма."""
        movie_update = MovieUpdate(
            name="Movie title",
            description="Movie description",
            production_year=datetime.now(tz=TIME_ZONE).year - 1,
            country="США",
            genre="Мелодрама",
        )

        for field_name, value in movie_update:
            if hasattr(self.movie, field_name):
                setattr(self.movie, field_name, value)

        self.assertEqual(self.movie.name, movie_update.name)
        self.assertEqual(self.movie.description, movie_update.description)
        self.assertEqual(self.movie.production_year, movie_update.production_year)
        self.assertEqual(self.movie.country, movie_update.country)
        self.assertEqual(self.movie.genre, movie_update.genre)

    def test_partial_update(self) -> None:
        """Проверка частичного обновления экземпляра фильма."""
        partial_updates = [
            ("field name: name", MoviePartialUpdate(name="Movie title")),
            (
                "field name: description",
                MoviePartialUpdate(description="Movie description"),
            ),
            ("field name: production_year", MoviePartialUpdate(production_year=2025)),
            ("field name: country", MoviePartialUpdate(country="Country")),
            ("field name: genre", MoviePartialUpdate(genre="Genre")),
        ]

        for msg, partial_update in partial_updates:
            with self.subTest(msg=msg):
                for field_name, value in partial_update.model_dump(
                    exclude_unset=True,
                ).items():
                    if hasattr(self.movie, field_name):
                        setattr(self.movie, field_name, value)

                    self.assertEqual(
                        getattr(partial_update, field_name),
                        getattr(self.movie, field_name),
                    )

    def test_partial_update_with_empty_instance(self) -> None:
        """Проверка частичного обновления экземпляра фильма с пустым экземпляром."""
        movie_partial_update = MoviePartialUpdate()
        movie = self.movie.model_copy()

        for field_name, value in movie_partial_update.model_dump(
            exclude_unset=True,
        ).items():
            if hasattr(self.movie, field_name):
                setattr(self.movie, field_name, value)

        self.assertEqual(movie.name, self.movie.name)
        self.assertEqual(movie.description, self.movie.description)
        self.assertEqual(movie.production_year, self.movie.production_year)
        self.assertEqual(movie.country, self.movie.country)
        self.assertEqual(movie.genre, self.movie.genre)

    def test_movie_create_slug_too_short(self) -> None:
        """Проверяет выброс исключения при слишком коротком слаге."""
        with self.assertRaises(ValidationError) as exc_info:
            MovieCreate(
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

    def test_movie_create_slug_too_short_with_regex(self) -> None:
        with self.assertRaisesRegex(
            ValidationError,
            expected_regex="String should have at least 3 characters",
        ):
            MovieCreate(
                name="sl",
                description="Some description",
                production_year=datetime.now(tz=TIME_ZONE).year,
                country="Россия",
                genre="Семейный",
                slug="some-slug",
            )
