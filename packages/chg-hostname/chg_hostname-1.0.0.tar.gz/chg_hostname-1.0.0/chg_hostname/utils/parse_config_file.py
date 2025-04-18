from ipaddress import ip_address
from .host_entry import HostRecord

def parse_config_file(lines: list[str]) -> list[HostRecord]:
    ip_table: list[HostRecord] = []

    for content in lines:
        content = content.strip()
        parts = content.split(",")
        ip = ip_address(parts[0])
        hostname = parts[1]

        ip_table.append(HostRecord(ip=ip, hostname=hostname))

    return ip_table
