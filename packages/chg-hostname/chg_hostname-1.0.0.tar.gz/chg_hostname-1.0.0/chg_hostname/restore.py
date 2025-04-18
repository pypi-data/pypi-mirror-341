from pathlib import Path
import typer
from pathlib import Path
from typing_extensions import Annotated
from rich.console import Console
from rich.prompt import Confirm
from chg_hostname.utils import print_table
from chg_hostname.utils.is_admin import check_if_admin


console = Console(log_time=False)
app = typer.Typer(
    rich_markup_mode="markdown",
)


def restore_backup(path: str, content: list[str]) -> None:
    """
    Oh, the delicate art of overwriting!

    Args:
        path (str): The *lucky* file that will receive the glorious content.
        content (list[str]): The pristine lines, ready to replace the current... *masterpiece*.
    """
    with open(path, "w") as file:
        for line in content:
            file.write(line + "\n")


@app.command()
def restore(
    path: Annotated[
        Path,
        typer.Option(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
            help="The path to the host file you wish to *restore* (and potentially regret).",
            show_default=False,
            rich_help_panel="Required",
        ),
    ] = Path("/etc/hosts"),
    backup_location: Annotated[
        Path,
        typer.Option(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
            help="The path to the backup file. Hopefully, it's what you intended to save.",
            rich_help_panel="Options",
        ),
    ] = Path("./hosts.backup"),
) -> None:
    """
    Like a phoenix rising from the ashes (or more accurately, a file being rudely replaced)

    this command will **obliterate** the current host file with the contents of your backup.
    Hope you *really* wanted that!
    """

    if path == backup_location:
        raise ValueError(
            "[bold red]:boom: Catastrophic Failure Imminent! :boom:\n"
            "You've specified the same path for both the original file and the backup location! "
            "[italic](Are you trying to create a paradox? Because that's how you create a paradox!)[/italic]\n"
            "Please provide distinct paths, unless you have a penchant for digital self-destruction."
        )

    path_to_file = Path(path)
    path_to_backup = Path(backup_location)
    check_if_admin()

    console.log(f"[info] :vampire: Examining the current state of [cyan]{path}[/cyan]:")

    content = path_to_file.read_text().splitlines(keepends=True)
    print_table(content)

    console.log(
        f"[info]:rewind: Peeking at the contents of the backup file [green]{backup_location}[/green]:"
    )

    backup_content = path_to_backup.read_text().splitlines()
    print_table(backup_content)
    confirm = Confirm.ask(
        "[warning]:rotating_light: [bold red]STOP! This is a destructive command![/bold red] :rotating_light:\n"
        f"You are about to [bold blink]OVERWRITE[/bold blink] the contents of [cyan]{path}[/cyan]\n"
        f"with the content from [green]{backup_location}[/green], [bold]REPLACING ALL PREVIOUS DATA![/bold]\n"
        "[question]Do you understand the irreversible nature of this operation and wish to proceed?",
        default=False,
    )
    if confirm:
        restore_backup(path.as_posix(), backup_content)
        console.log(
            "[check_mark]:sparkles: File updated successfully! The past has become the present! :sparkles:"
        )

    else:
        console.log(
            "[cross]:lock: Restoration aborted. Your original file remains untouched (for now...)."
        )
