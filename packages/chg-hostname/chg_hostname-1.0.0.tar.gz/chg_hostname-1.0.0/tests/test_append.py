from chg_hostname.replace_loopback import LOOPBACK_ADDRESS, replace_loopback_address
from chg_hostname.utils.host_entry import NetworkConfig
from ipaddress import ip_address
import pytest


@pytest.fixture
def sample_config() -> NetworkConfig:
    return NetworkConfig(
        loopback_ip="192.168.0.10",
        host_entries=[
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
    )


def test_format_host_records(sample_config: NetworkConfig) -> None:
    ip_table = replace_loopback_address(sample_config)

    expected = [
        (LOOPBACK_ADDRESS, "pihole.lan"),
        (ip_address("192.168.0.3"), "rome.lan"),
        (ip_address("192.168.0.3"), "kube.master.lan"),
    ]

    for index, (expected_ip, expected_hostname) in enumerate(expected):
        record = ip_table[index]
        assert record.ip == expected_ip, f"Row {index} IP mismatch"
        assert record.hostname == expected_hostname, f"Row {index} hostname mismatch"

    assert len(ip_table) == len(sample_config.host_entries)
