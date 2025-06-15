import logging

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
    Film,
    FilmCreate,
    FilmUpdate,
    FilmPartialUpdate,
)

log = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_FILMS,
    decode_responses=True,
)


class FilmStorage(BaseModel):

    def save_film(self, film: Film) -> None:
        redis.hset(
            name=config.REDIS_FILMS_HASH_NAME,
            key=film.slug,
            value=film.model_dump_json(),
        )

    def get(self) -> list[Film]:
        return [
            Film.model_validate_json(film)
            for film in redis.hvals(name=config.REDIS_FILMS_HASH_NAME)
        ]

    def get_by_slug(self, slug: str) -> Film | None:
        film = redis.hget(
            name=config.REDIS_FILMS_HASH_NAME,
            key=slug,
        )
        if film is not None:
            film = Film.model_validate_json(film)

        return film

    def create(self, film_create: FilmCreate) -> Film:
        film = Film(
            **film_create.model_dump(),
        )
        self.save_film(film=film)
        log.info("Создано описание фильма '%s' ", film.name)

        return film

    def delete_by_slug(self, slug: str) -> None:
        redis.hdel(
            config.REDIS_FILMS_HASH_NAME,
            slug,
        )

    def delete(self, film: Film) -> None:
        self.delete_by_slug(film.slug)

    def update(
        self,
        film: Film,
        film_in: FilmUpdate,
    ) -> Film:
        for field_name, value in film_in:
            setattr(film, field_name, value)
        self.save_film(film=film)

        return film

    def update_partial(
        self,
        film: Film,
        film_in: FilmPartialUpdate,
    ) -> Film:
        for field_name, value in film_in.model_dump(exclude_unset=True).items():
            setattr(film, field_name, value)
        self.save_film(film=film)

        return film


storage = FilmStorage()
