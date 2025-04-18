from ipaddress import IPv4Address, IPv6Address
from typing import List
from chg_hostname.replace_loopback import replace_loopback_address
from chg_hostname.utils.host_entry import HostRecord, NetworkConfig
from rich.console import Console

from chg_hostname.utils.table import create_ip_table

json = {
    "loopback_ip": "192.168.0.10",
    "host_entries": [
        {"ip": "192.168.0.10", "hostname": "pihole.lan"},
        {"ip": "192.168.0.3", "hostname": "rome.lan"},
        {"ip": "192.168.0.3", "hostname": "kube.master.lan"},
        {"ip": "192.168.0.14", "hostname": "grace.lan"},
        {"ip": "192.168.0.14", "hostname": "kube.master-2.lan"},
        {"ip": "192.168.0.19", "hostname": "atlantis.lan"},
        {"ip": "192.168.0.19", "hostname": "kube.node.lan"},
        {"ip": "192.168.0.36", "hostname": "italy.lan"},
        {"ip": "192.168.0.36", "hostname": "kube.node-2.lan"},
    ],
}


if __name__ == "__main__":
    replace_loopback_address(NetworkConfig(**json))
