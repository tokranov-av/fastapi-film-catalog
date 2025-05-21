import logging
import time

from pydantic import (
    BaseModel,
    ValidationError,
)

from core.config import FILMS_STORAGE_FILEPATH
from schemas.film import (
    Film,
    FilmCreate,
    FilmUpdate,
    FilmPartialUpdate,
)

log = logging.getLogger(__name__)


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

    def get(self) -> list[Film]:
        return list(self.slug_to_film.values())

    def get_by_slug(self, slug: str) -> Film | None:
        return self.slug_to_film.get(slug)

    def create(self, film_create: FilmCreate) -> Film:
        film = Film(
            **film_create.model_dump(),
        )
        self.slug_to_film[film.slug] = film

        return film

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_film.pop(slug, None)

    def delete(self, film: Film) -> None:
        self.delete_by_slug(film.slug)

    def update(
        self,
        film: Film,
        film_in: FilmUpdate,
    ) -> Film:
        for field_name, value in film_in:
            setattr(film, field_name, value)

        return film

    def update_partial(
        self,
        film: Film,
        film_in: FilmPartialUpdate,
    ) -> Film:
        for field_name, value in film_in.model_dump(exclude_unset=True).items():
            setattr(film, field_name, value)

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
