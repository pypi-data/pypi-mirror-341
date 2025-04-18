from rich.table import Table
from rich.console import Console

console = Console()


def create_ip_table() -> Table:
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("IPs", style="dim", width=12)
    table.add_column("Hosts")

    return table
