__all__ = ("app",)

import typer

from .data_preparation import app as load_data_app
from .hello import app as hello_app
from .tokens import app as tokens_app

app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.callback()
def callback() -> None:
    """Some CLi management commands."""


app.add_typer(hello_app)
app.add_typer(tokens_app)
app.add_typer(load_data_app)
