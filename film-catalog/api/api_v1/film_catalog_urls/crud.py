__all__ = ("MovieAlreadyExistsError", "storage")

import logging
from typing import cast

from pydantic import (
    BaseModel,
)
from redis import (
    Redis,
)

from core import (
    config,
)
from schemas.film import (
    Movie,
    MovieCreate,
    MoviePartialUpdate,
    MovieUpdate,
)

log = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_MOVIES,
    decode_responses=True,
)


class MovieBaseError(Exception):
    """Base exception for movie CRUD actions."""


class MovieAlreadyExistsError(MovieBaseError):
    """Raised when a movie already exists."""


class MovieStorage(BaseModel):
    def save_movie(self, movie: Movie) -> None:
        redis.hset(
            name=config.REDIS_MOVIES_HASH_NAME,
            key=movie.slug,
            value=movie.model_dump_json(),
        )

    def get(self) -> list[Movie]:
        return [
            Movie.model_validate_json(movie)
            for movie in redis.hvals(name=config.REDIS_MOVIES_HASH_NAME)
        ]

    def get_by_slug(self, slug: str) -> Movie | None:
        if data := redis.hget(
            name=config.REDIS_MOVIES_HASH_NAME,
            key=slug,
        ):
            assert isinstance(data, str)
            return Movie.model_validate_json(data)

        return None

    def exists(self, slug: str) -> bool:
        return cast(
            bool,
            redis.hexists(
                name=config.REDIS_MOVIES_HASH_NAME,
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
            config.REDIS_MOVIES_HASH_NAME,
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


storage = MovieStorage()
