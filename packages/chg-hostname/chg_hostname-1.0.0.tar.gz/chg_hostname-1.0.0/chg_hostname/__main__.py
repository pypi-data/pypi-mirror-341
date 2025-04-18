import typer
from rich.console import Console
from chg_hostname.backup import app as backup_app
from chg_hostname.restore import app as restore_app
from chg_hostname.version import app as version_app
from chg_hostname.run import app as run_app

console = Console()
app = typer.Typer(
    help="""
    Yet another tool to **fiddle** with your host file. 🕸️  Because who doesn't enjoy the
    thrill of potentially **breaking their internet connectivity**?📵 --- Features include
    backing up 💾 (`as if that will actually save you`), restoring 🕰️ (good luck with that 🤔),
    and modifying ✍️ (**prepare for unexpected outcomes** 🔮).
    """,
    rich_markup_mode="markdown",
)
app.add_typer(typer_instance=version_app)
app.add_typer(typer_instance=backup_app)
app.add_typer(typer_instance=restore_app)
app.add_typer(typer_instance=run_app)


def main() -> None:
    """
    The grand orchestrator! This is where the Typer application comes to life,
    gracefully incorporating all the subcommands. A true masterpiece of command-line interface design.
    """
    app()


if __name__ == "__main__":
    main()
