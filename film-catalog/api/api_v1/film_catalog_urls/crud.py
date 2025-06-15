import logging

from pydantic import (
    BaseModel,
    ValidationError,
)
from redis import Redis

from core import config
from core.config import FILMS_STORAGE_FILEPATH
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
    slug_to_film: dict[str, Film] = {}

    def save_state(self) -> None:
        FILMS_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))
        log.info(f"Информация о фильме сохранена.")

    @classmethod
    def from_state(cls) -> "FilmStorage":
        if not FILMS_STORAGE_FILEPATH.exists():
            log.info("Файл хранилища отсутствует")

            return FilmStorage()

        return cls.model_validate_json(FILMS_STORAGE_FILEPATH.read_text())

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

    def init_storage_from_state(self) -> None:
        try:
            data = self.from_state()
        except ValidationError:
            self.save_state()
            log.warning("Перезаписан файл хранилища из-за ошибки проверки")
        else:
            self.slug_to_film.update(
                data.slug_to_film,
            )
            log.info("Хранилище заполнено данными из файла хранилища")


storage = FilmStorage()
