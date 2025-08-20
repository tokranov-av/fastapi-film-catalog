from collections.abc import Generator
from typing import ClassVar
from unittest import TestCase

import pytest

from api.api_v1.film_catalog_urls.crud import (
    MovieAlreadyExistsError,
    storage,
)
from schemas.film import (
    Movie,
    MovieCreate,
    MoviePartialUpdate,
    MovieUpdate,
)
from testing.utils import (
    create_movie_random_slug,
)


@pytest.fixture
def movie() -> Generator[Movie]:
    movie = create_movie_random_slug()
    yield movie
    storage.delete(movie)


class FilmStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.movie = create_movie_random_slug()
        self.expected_description = "Another description"
        self.expected_genre = "Another genre"

    def tearDown(self) -> None:
        storage.delete(self.movie)

    def test_update(self) -> None:
        film_update = MovieUpdate(**self.movie.model_dump())
        film_update.description = self.expected_description
        film_update.genre = self.expected_genre

        updated_film = storage.update(
            movie=self.movie,
            movie_in=film_update,
        )

        self.assertEqual(self.expected_description, updated_film.description)
        self.assertEqual(self.expected_genre, updated_film.genre)

    def test_partial_update(self) -> None:
        film_partial_update = MoviePartialUpdate(
            description=self.expected_description,
            genre=self.expected_genre,
        )
        expected_name = self.movie.name

        partial_updated_movie = storage.update_partial(
            movie=self.movie,
            movie_in=film_partial_update,
        )

        self.assertEqual(self.expected_description, partial_updated_movie.description)
        self.assertEqual(self.expected_genre, partial_updated_movie.genre)
        self.assertEqual(expected_name, partial_updated_movie.name)


class FilmStorageGetFilmsTestCase(TestCase):
    FILMS_COUNT = 3
    movies: ClassVar[list[Movie]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.movies = [create_movie_random_slug() for _ in range(cls.FILMS_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for movie in cls.movies:
            storage.delete(movie)

    def test_get_list(self) -> None:
        expected_slugs = {movie.slug for movie in self.movies}
        expected_diff = set[str]()

        movies = storage.get()
        films_slugs = {movie.slug for movie in movies}
        diff = expected_slugs - films_slugs

        self.assertEqual(expected_diff, diff)

    def test_get_by_slug(self) -> None:
        for movie in self.movies:
            with self.subTest(
                slug=movie.slug,
                msg=f"Validate can get slug {movie.slug!r}",
            ):
                db_film = storage.get_by_slug(slug=movie.slug)

                self.assertEqual(db_film, movie)


def test_create_or_raise_if_exists(movie: Movie) -> None:
    movie_create = MovieCreate(**movie.model_dump())

    with pytest.raises(
        MovieAlreadyExistsError,
        match=movie.slug,
    ) as exc_info:
        storage.create_or_raise_if_exists(movie_create)

    assert movie_create.slug in exc_info.value.args[0]
