import typer
from rich.console import Console

console = Console()
app = typer.Typer()


@app.command()
def version() -> None:
    """
    Ah, the coveted version command! It unveils the *highly classified* version
    of this magnificent tool. Prepare to be amazed! :sparkles:

    * It bravely announces the current version.
    * That's pretty much it. Don't expect fireworks.

    ---

    For those who crave more (and let's be honest, who doesn't?), you can explore
    the [Typer docs website](https://typer.tiangolo.com). Knock yourself out.
    """
    console.print("cgh-hostname Version 1.0")
