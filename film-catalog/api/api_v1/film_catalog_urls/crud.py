from pydantic import BaseModel

from schemas.film import (
    Film,
    FilmCreate,
)


class FilmStorage(BaseModel):
    slug_to_film: dict[str, Film] = {}

    def get(self) -> list[Film]:
        return list(self.slug_to_film.values())

    def get_by_slug(self, slug: str) -> Film | None:
        return self.slug_to_film.get(slug)

    def create(self, film_create: FilmCreate) -> Film:
        film = Film(**film_create.model_dump())
        self.slug_to_film[film.slug] = film

        return film


storage = FilmStorage()

storage.create(
    FilmCreate(
        slug="diamond_hand",
        name="Бриллиантовая рука",
        description=(
            "Контрабандисты гоняются за примерным семьянином. Народная комедия с элементами абсурда от Леонида Гайдая."
        ),
        production_year=1968,
        country="СССР",
        genre="комедия, криминал",
    )
)
storage.create(
    FilmCreate(
        slug="avatar",
        name="Аватар",
        description=(
            "Бывший морпех Джейк Салли получает задание совершить путешествие в несколько световых лет к базе землян"
            " на планете Пандора, где корпорации добывают редкий минерал, имеющий огромное значение для выхода"
            " Земли из энергетического кризиса."
        ),
        production_year=2009,
        country="США, Великобритания",
        genre="фантастика, боевик, драма, приключения",
    )
)
storage.create(
    FilmCreate(
        slug="home_alone",
        name="Один дома",
        description=(
            "Американское семейство отправляется из Чикаго в Европу, но в спешке сборов бестолковые родители забывают"
            " дома... одного из своих детей. Юное создание, однако, не теряется и демонстрирует чудеса"
            " изобретательности. И когда в дом залезают грабители, им приходится не раз пожалеть о встрече"
            " с милым крошкой."
        ),
        production_year=1990,
        country="США",
        genre="комедия, семейный",
    )
)
