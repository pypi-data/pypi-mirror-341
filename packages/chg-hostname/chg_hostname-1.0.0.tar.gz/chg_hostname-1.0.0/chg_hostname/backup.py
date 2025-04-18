from pathlib import Path
from rich.console import Console
import typer
from rich.prompt import Prompt, Confirm
from typing_extensions import Annotated
from chg_hostname.utils import print_table
from chg_hostname.utils import FileUtil

console = Console()
app = typer.Typer(rich_markup_mode="markdown")


def backup_file(host_path: str, content: list[str]) -> None:
    """
    This function bravely takes a file's content and, against all odds,
    writes it to another location. A true hero!

    Args:
        host_path (str): The destination path for the backup. Let's hope it's writable.
        content (list[str]): The precious data to be immortalized in the backup.
    """
    try:
        with open(host_path, "w") as file:
            for line in content:
                file.write(line)
    except FileNotFoundError:
        console.log(f"[red]File not found: {host_path}[/red]")
    except PermissionError:
        console.log(f"[red]Permission denied: {host_path}[/red]")
    except Exception as e:
        console.log(f"[red]An error occurred: {e}[/red]")


@app.command()
def backup(
    path: Annotated[
        Path,
        typer.Option(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
            help="The path to the file you wish to... *preserve*.",
        ),
    ] = Path("/etc/hosts"),
    backup_path: Annotated[
        Path,
        typer.Argument(
            exists=False,
            file_okay=True,
            dir_okay=False,
            writable=True,
            readable=True,
            resolve_path=True,
            help='The majestic location where the backup will reside. Defaults to "./hosts.backup". How convenient!',
            rich_help_panel="Optional",
        ),
    ] = Path("./hosts.backup"),
) -> None:
    """
    **Prepare for the awe-inspiring backup command!**

    It takes a file **(hopefully your host file)**
    and makes a copy. Because who doesn't love a safety net?
    """

    if path == backup_path:
        raise ValueError(
            "[bold red] Error: [/bold red] The host file path and the backup file path cannot be the same. "
            "Backing up a file to itself? That's like trying to fold a fitted sheet – utterly pointless."
        )

    if backup_path.exists():
        console.log(
            "[warning]:skull: [bold yellow]Hold on there, Captain Overwrite![/bold yellow] :skull:\n"
            f"It seems a backup already exists at [cyan]{backup_path}[/cyan]. Take a gander at its current state:"
        )
        backup_content = backup_path.read_text().splitlines()
        print_table(backup_content)

        confirm_overwrite = Confirm.ask(
            "[question] [bold red]Are you absolutely sure[/bold red] you want to [bold blink]obliterate[/bold blink] "
            "the current backup with a new one? [dim](Think of the lost data! The digital tears!)[/dim]",
            default=False,
        )

        if confirm_overwrite:
            console.log("[info]:gear: Preparing to overwrite the existing backup...")
            content = FileUtil(path.as_posix()).get_content()
            console.log("[info]:eyes: Current content of the file you're backing up:")
            print_table(content)

            confirm = Confirm.ask(
                f"[warning] :fire: Last chance! You are about to [bold red]irrevocably[/bold red] overwrite the backup at "
                f"[cyan]{backup_path}[/cyan] with the content above. Proceed? [dim](No take-backsies!)[/dim]",
                default=False,
            )
            if confirm:
                backup_file(backup_path.as_posix(), content)
                console.log(
                    "[check_mark]:tada: Backup completed (and the old one? Gone with the wind!).[/check_mark]"
                )
            else:
                console.log(
                    "[cross]:no_entry_sign: Backup operation aborted. The old backup lives to see another day!"
                )
        else:
            console.log(
                "[cross]:sleeping_face: Backup overwrite cancelled. The existing backup remains safe and sound (for now)."
            )
    else:
        console.print(
            f"[info]:new: No existing backup found. Creating a shiny new one at [green]{backup_path}[/green]..."
        )
        content = FileUtil(path.as_posix()).get_content()
        print_table(content)
        confirm = typer.confirm(
            f"[question] You will backup your file at [cyan]{backup_path}[/cyan]. Ready to immortalize this moment?",
            default=True,
        )
        if confirm:
            backup_file(backup_path.as_posix(), content)
            console.print(
                f"[check_mark]:floppy_disk: Backup created successfully at [green]{backup_path}[/green]!"
            )
        else:
            console.print(
                "[cross]:no_entry_sign: Backup operation aborted. No backup was created."
            )
