__all__ = ("app",)

import json

import typer
from rich import print

from api.api_v1.film_catalog_urls.crud import (
    MovieAlreadyExistsError,
    storage,
)
from core.config import BASE_DIR
from schemas.film import MovieCreate

app = typer.Typer(
    name="data_prep",
    help="[blue]Database data management[/blue]",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command(name="load_from_file")
def load_data_from_file() -> None:
    """Загрузка базы данных данными из файла."""
    file_path = BASE_DIR / "films.json"
    with file_path.open(encoding="utf-8") as file:
        data = json.load(file)

    for movies in data.values():
        for movie in movies.values():
            try:
                storage.create_or_raise_if_exists(MovieCreate(**movie))
                print(
                    f"[green]A movie with the slug {movie['slug']} has been"
                    f" successfully added to the database.[/green]",
                )
            except MovieAlreadyExistsError:
                print(
                    f"[red]A movie with the slug [bold]{movie['slug']}[/bold]"
                    f" already exists.[/red]",
                )


@app.command(name="delete_by_slug")  # 👈 добавить команду удаления
def delete_movie_by_slug(slug: str) -> None:
    """Удаление фильма по слагу."""
    movie = storage.get_by_slug(slug=slug)
    if not movie:
        print(
            f"[red]A movie with the slug [bold]{movie['slug']}[/bold] not found.[/red]",
        )
    else:
        storage.delete_by_slug(slug=movie.slug)
        print(f"[green]The film with the slug [bold]{slug}[/bold] was removed[/green]")
