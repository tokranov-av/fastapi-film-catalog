from typing import Annotated

from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    status,
    Depends,
)
from schemas.film import Film

app = FastAPI(
    title="Film Catalog API",
)


FILMS = [
    Film(
        id=1,
        name="Бриллиантовая рука",
        description=(
            "Контрабандисты гоняются за примерным семьянином. Народная комедия с элементами абсурда от Леонида Гайдая"
        ),
        production_year=1968,
        country="СССР",
        genre="комедия, криминал",
    ),
    Film(
        id=2,
        name="Аватар",
        description=(
            "Бывший морпех Джейк Салли получает задание совершить путешествие в несколько световых лет к базе землян"
            " на планете Пандора, где корпорации добывают редкий минерал, имеющий огромное значение для выхода"
            " Земли из энергетического кризиса."
        ),
        production_year=2009,
        country="США, Великобритания",
        genre="фантастика, боевик, драма, приключения",
    ),
    Film(
        id=3,
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
    ),
]


def prefetch_film(movie_id: int) -> Film:
    film: Film | None = next(
        (film for film in FILMS if film.id == movie_id),
        None,
    )

    if film:
        return film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with id = {movie_id} not found",
    )


@app.get("/")
def read_root(
    request: Request,
    name: str = "World",
):
    docs_url = request.url.replace(path="/docs", query="")

    return {
        "message": f"Hello {name}",
        "docs": str(docs_url),
    }


@app.get(
    path="/films/",
    response_model=list[Film],
)
def get_list_of_films():
    return FILMS


@app.get(path="/films/{movie_id}/")
def read_movie_description(
    film: Annotated[
        Film,
        Depends(prefetch_film),
    ],
):
    return film
