import typer
from pathlib import Path
from rich.console import Console
from typing_extensions import Annotated
from chg_hostname.parse_host import parse_host_file
from chg_hostname.replace_loopback import replace_loopback_address
from chg_hostname.utils import FileUtil, print_ip_table, NetworkConfig
from chg_hostname.backup import backup_file
from chg_hostname.append import append
import json
import socket


from chg_hostname.utils.get_ip import get_primary_local_ip
from chg_hostname.utils.is_admin import check_if_admin

console = Console()
app = typer.Typer(
    rich_markup_mode="markdown",
)


file_write_check = Annotated[
    Path,
    typer.Option(
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=True,
        resolve_path=True,
    ),
]


def load_network_config(path: str) -> NetworkConfig:
    """
    Like a seasoned archaeologist unearthing ancient scrolls, this function
    carefully reads and deciphers your JSON configuration file, transforming
    its cryptic contents into a glorious NetworkConfig object. Prepare for enlightenment!

    Args:
        path (str): The path to the JSON configuration file. Handle with reverence.

    Returns:
        NetworkConfig: The magnificent NetworkConfig object, born from the depths of your JSON.
    """
    try:
        with open(path) as file:
            json_file = json.load(file)
        return NetworkConfig(**json_file)
    except Exception:
        raise ValueError("Invalid JSON format in config file. Please check the syntax.")


@app.command()
def run(
    host_path: Annotated[
        Path,
        typer.Option(
            "--host-path",
            "-H",
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
            help="The path to your system's host file. Proceed with caution, brave adventurer.",
            rich_help_panel="Required",
        ),
    ] = Path("/etc/hosts"),
    config_path: Annotated[
        Path,
        typer.Option(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=True,
            readable=True,
            resolve_path=True,
            help="The path to the JSON configuration file containing the new host entries.",
            rich_help_panel="Options",
        ),
    ] = Path("./hosts.json"),
    backup_path: Annotated[
        Path,
        typer.Option(
            exists=False,
            file_okay=True,
            dir_okay=False,
            writable=True,
            readable=True,
            resolve_path=True,
            help="The path where a backup of your host file will be safely stored (hopefully).",
            rich_help_panel="Options",
        ),
    ] = Path("./backup.hosts"),
    backup: Annotated[bool, typer.Option(rich_help_panel="Options")] = True,
) -> None:
    """
    Behold! The **RUN** command! The culmination of all your hard work!

    This majestic function orchestrates the entire process: backing up your precious
    host file, parsing the arcane configurations, replacing those pesky loopback
    addresses, and finally, appending the new entries with the grace of a digital calligrapher.
    Prepare for the magic to unfold! :sparkles:
    """
    hostname = socket.gethostname()
    console.log(get_primary_local_ip())
    console.log(hostname)

    check_if_admin()

    if host_path == config_path:
        raise ValueError(
            "[bold red]Error:[/bold red] The host file path and the configuration file path cannot be the same. "
            "Are you trying to make the file eat itself? That's not how this works."
        )

    if host_path == backup_path:
        raise ValueError(
            "[bold red]Error:[/bold red] The host file path and the backup file path cannot be the same. "
            "Backing up a file to itself? That's like trying to fold a fitted sheet – utterly pointless."
        )

    host_path_content = host_path.read_text().splitlines(keepends=True)

    if backup:
        if backup_path.exists():
            backup_confirm = typer.confirm(
                "This file is already backed up or there is data in here, do you want to proceed?"
            )
            if backup_confirm:
                backup_file(backup_path.as_posix(), host_path_content)
            else:
                console.log("Thee recklessly trying")
        else:
            backup_file(backup_path.as_posix(), host_path_content)

    ip_table = load_network_config(path=config_path.as_posix())
    extra_ips = replace_loopback_address(ip_table)
    host_ip_table = parse_host_file(host_path)

    console.log("[bold magenta]Original hostname file:[/bold magenta]")
    print_ip_table(host_ip_table)

    console.log("[bold magenta]Host entries to append:[/bold magenta]")
    print_ip_table(extra_ips)

    confirm = typer.confirm(
        "Are you absolutely, positively sure you want to append these entries?"
    )

    if confirm:
        append(
            host_path.as_posix(),
            NetworkConfig(loopback_ip=ip_table.loopback_ip, host_entries=extra_ips),
        )
        console.log("[green]Successfully appended new host entries![/green]")
    else:
        console.log(
            "[yellow]Operation aborted. Your host file remains untouched (for now!).[/yellow]"
        )
