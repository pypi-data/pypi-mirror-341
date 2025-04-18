from typing import List
from rich.console import Console
from .table import create_ip_table
from .parse_config_file import HostRecord

console = Console()


def print_ip_table(ip_table: List[HostRecord]) -> None:
    table = create_ip_table()

    for entry in ip_table:
        table.add_row(entry.ip.exploded, entry.hostname)

    console.log(table)


def print_table(content: List[str]) -> None:
    table = create_ip_table()

    for lines in content:
        if lines.startswith("#"):
            continue

        parts = lines.split()
        if len(parts) >= 2:
            # ip, hostname = parts
            ip = parts[0]
            hostname = parts[1]
            table.add_row(ip, hostname)

    console.log(table)
