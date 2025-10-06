__all__ = ("MovieAlreadyExistsError", "storage")

import logging
from typing import cast

from pydantic import (
    BaseModel,
)
from redis import (
    Redis,
)

from core.config import (
    settings,
)
from schemas.film import (
    Movie,
    MovieCreate,
    MoviePartialUpdate,
    MovieUpdate,
)

log = logging.getLogger(__name__)

redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.movies,
    decode_responses=True,
)


class MovieBaseError(Exception):
    """Base exception for movie CRUD actions."""


class MovieAlreadyExistsError(MovieBaseError):
    """Raised when a movie already exists."""


class MovieStorage(BaseModel):
    hash_name: str

    def save_movie(self, movie: Movie) -> None:
        redis.hset(
            name=self.hash_name,
            key=movie.slug,
            value=movie.model_dump_json(),
        )

    def get(self) -> list[Movie]:
        return [
            Movie.model_validate_json(movie)
            for movie in redis.hvals(name=self.hash_name)
        ]

    def get_by_slug(self, slug: str) -> Movie | None:
        if data := redis.hget(
            name=self.hash_name,
            key=slug,
        ):
            assert isinstance(data, str)
            return Movie.model_validate_json(data)

        return None

    def exists(self, slug: str) -> bool:
        return cast(
            bool,
            redis.hexists(
                name=self.hash_name,
                key=slug,
            ),
        )

    def create(self, movie_create: MovieCreate) -> Movie:
        movie = Movie(
            **movie_create.model_dump(),
        )
        self.save_movie(movie=movie)
        log.info("Создано описание фильма '%s' ", movie.name)

        return movie

    def create_or_raise_if_exists(self, movie_create: MovieCreate) -> Movie:
        if not self.exists(movie_create.slug):
            return self.create(movie_create)

        msg = f"Movie with slug {movie_create.slug} already exists"
        raise MovieAlreadyExistsError(msg)

    def delete_by_slug(self, slug: str) -> None:
        redis.hdel(
            self.hash_name,
            slug,
        )

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(movie.slug)

    def update(
        self,
        movie: Movie,
        movie_in: MovieUpdate,
    ) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        self.save_movie(movie=movie)

        return movie

    def update_partial(
        self,
        movie: Movie,
        movie_in: MoviePartialUpdate,
    ) -> Movie:
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        self.save_movie(movie=movie)

        return movie


storage = MovieStorage(
    hash_name=settings.redis.collections_names.movies_hash,
)
