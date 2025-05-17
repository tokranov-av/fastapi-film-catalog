import os

from pydantic import (
    BaseModel,
    ValidationError,
)

from schemas.film import (
    Film,
    FilmCreate,
    FilmUpdate,
    FilmPartialUpdate,
)


class FilmStorage(BaseModel):
    slug_to_film: dict[str, Film] = {}
    file_path: str = os.path.join(os.path.dirname(__file__), "data.json")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._read_file()

    def _read_file(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            data = ""
            for line in file:
                line = line.replace("\n", "").strip()
                if line.startswith("{"):
                    data = ""

                data += line

                if data.endswith("}"):
                    try:
                        film = Film.model_validate_json(data)
                        self.slug_to_film[film.slug] = film
                        data = ""
                    except ValidationError as e:
                        pass

    def get(self) -> list[Film]:
        return list(self.slug_to_film.values())

    def get_by_slug(self, slug: str) -> Film | None:
        return self.slug_to_film.get(slug)

    def create(self, film_create: FilmCreate) -> Film:
        film = Film(**film_create.model_dump())
        self.slug_to_film[film.slug] = film

        with open(self.file_path, "a", encoding="utf-8") as file:
            file.write(film.model_dump_json(indent=2) + "\n")

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


storage = FilmStorage()
