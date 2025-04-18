from rich.console import Console
from chg_hostname.utils import HostRecord, NetworkConfig


console = Console()

LOOPBACK_ADDRESS = "127.0.0.1"


def append(host_file_path: str, net_config: NetworkConfig) -> None:
    """
    Ah, the gentle art of appending! This function delicately adds new host entries
    to the end of your host file, with the occasional decorative separator. How thoughtful!

    Args:
        host_file_path (str): The path to the host file, patiently awaiting new additions.
        net_config (NetworkConfig): The network configuration, brimming with host entries eager to join the party.
    """
    with open(host_file_path, "a") as file:
        table_iterator = iter(net_config.host_entries)

        file.write("# ============= \n")
        initial_value = next(table_iterator)

        file.write(f"{initial_value.ip} \t{initial_value.hostname} \n")

        for content in table_iterator:
            if initial_value.ip == content.ip:
                file.write(f"{content.ip} \t{content.hostname} \n")
            else:
                file.write("# ============= \n")
                file.write(f"{content.ip} \t{content.hostname} \n")
                initial_value = HostRecord(ip=content.ip, hostname=content.hostname)
