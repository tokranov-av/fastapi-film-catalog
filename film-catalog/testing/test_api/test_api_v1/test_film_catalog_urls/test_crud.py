from collections.abc import Generator
from typing import ClassVar
from unittest import TestCase

import pytest

from api.api_v1.film_catalog_urls.crud import (
    FilmAlreadyExistsError,
    storage,
)
from schemas.film import (
    Film,
    FilmCreate,
    FilmPartialUpdate,
    FilmUpdate,
)
from testing.utils import (
    create_film,
)


@pytest.fixture
def film() -> Generator[Film]:
    film = create_film()
    yield film
    storage.delete(film)


class FilmStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.film = create_film()
        self.expected_description = "Another description"
        self.expected_genre = "Another genre"

    def tearDown(self) -> None:
        storage.delete(self.film)

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


class FilmStorageGetFilmsTestCase(TestCase):
    FILMS_COUNT = 3
    films: ClassVar[list[Film]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.films = [create_film() for _ in range(cls.FILMS_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for film in cls.films:
            storage.delete(film)

    def test_get_list(self) -> None:
        expected_slugs = {film.slug for film in self.films}
        expected_diff = set[str]()

        films = storage.get()
        films_slugs = {film.slug for film in films}
        diff = expected_slugs - films_slugs

        self.assertEqual(expected_diff, diff)

    def test_get_by_slug(self) -> None:
        for film in self.films:
            with self.subTest(
                slug=film.slug,
                msg=f"Validate can get slug {film.slug!r}",
            ):
                db_film = storage.get_by_slug(slug=film.slug)

                self.assertEqual(db_film, film)


def test_create_or_raise_if_exists(film: Film) -> None:
    film_create = FilmCreate(**film.model_dump())

    with pytest.raises(
        FilmAlreadyExistsError,
        match=film.slug,
    ) as exc_info:
        storage.create_or_raise_if_exists(film_create)

    assert film_create.slug in exc_info.value.args[0]
