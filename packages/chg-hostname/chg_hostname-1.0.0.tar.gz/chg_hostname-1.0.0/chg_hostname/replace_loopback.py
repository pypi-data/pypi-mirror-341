from typing import List
from chg_hostname.utils.host_entry import HostRecord, NetworkConfig
from ipaddress import ip_address, IPv4Address, IPv6Address


LOOPBACK_ADDRESS = ip_address("127.0.0.1")


def is_same_ip(
    ip: IPv4Address | IPv6Address, ip_to_compare: IPv4Address | IPv6Address
) -> bool:
    """
    A profound function that determines if two IP addresses are, in fact, the same.
    Groundbreaking stuff, I know.

    Args:
        ip (IPv4Address | IPv6Address): The first IP address for this momentous comparison.
        ip_to_compare (IPv4Address | IPv6Address): The second IP address, eagerly awaiting judgment.

    Returns:
        bool: True if they are the same, False otherwise. Prepare for the truth!
    """
    return ip == ip_to_compare


def create_host_record(
    host_record: HostRecord, loopback_ip: IPv4Address | IPv6Address
) -> HostRecord:
    """
    Like a meticulous scribe, this function takes a host record and, under certain
    conditions (a loopback IP match, no less!), it performs the astonishing feat
    of replacing the IP address. Prepare to be amazed by this transformation!

    Args:
        host_record (HostRecord): The original host record, ripe for potential modification.
        loopback_ip (IPv4Address | IPv6Address): The IP address we're looking for. The target!

    Returns:
        HostRecord: The (potentially) modified host record. Handle with care.
    """
    if is_same_ip(host_record.ip, loopback_ip):
        return HostRecord(ip=LOOPBACK_ADDRESS, hostname=host_record.hostname)
    else:
        return HostRecord(ip=host_record.ip, hostname=host_record.hostname)


def replace_loopback_address(net_config: NetworkConfig) -> List[HostRecord]:
    """
    The mastermind behind the loopback replacement operation! It iterates through
    a network configuration and, with surgical precision, swaps out any matching
    IP addresses with the designated loopback address. A true digital artist at work!

    Args:
        net_config (NetworkConfig): The network configuration, containing all the juicy host entries.

    Returns:
        List[HostRecord]: A list of host records, now potentially sporting a brand new loopback IP.
    """
    host_records: List[HostRecord] = []

    table_iterator = iter(net_config.host_entries)
    previous_entry = next(table_iterator)

    host_records.append(create_host_record(previous_entry, net_config.loopback_ip))

    for content in table_iterator:
        if is_same_ip(previous_entry.ip, content.ip):
            host_records.append(create_host_record(content, net_config.loopback_ip))
        else:
            previous_entry = HostRecord(ip=content.ip, hostname=content.hostname)
            host_records.append(create_host_record(content, net_config.loopback_ip))
    return host_records
