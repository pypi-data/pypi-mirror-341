from ipaddress import ip_address
from pathlib import Path
from typing import List

from chg_hostname.utils.host_entry import HostRecord


def parse_host_file(path: Path) -> List[HostRecord]:
    """
    Like a diligent little ant, this function crawls through your host file
    and meticulously extracts the IP addresses and hostnames. Comments? We don't do comments here.

    Args:
        path (Path): The sacred path to the host file.

    Returns:
        List[HostRecord]: A list of beautifully parsed HostRecord objects. Aren't they lovely?
    """
    content = path.read_text().splitlines()
    host_records: List[HostRecord] = []

    for lines in content:
        if lines.startswith("#"):
            continue

        parts = lines.split()

        if len(parts) >= 2:
            ip = ip_address(parts[0])
            hostname = parts[1]
            host_records.append(HostRecord(ip=ip, hostname=hostname))
    return host_records
