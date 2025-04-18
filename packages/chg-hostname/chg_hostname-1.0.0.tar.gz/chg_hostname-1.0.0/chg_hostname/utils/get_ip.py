import socket

RANDOM_PORT = 1


def get_primary_local_ip(
    fallback_address: str = "127.0.0.1", fake_address: str = "10.0.0.0"
) -> str:
    """
    Returns the IP address of the primary outbound interface without sending packets.

    Parameters:
        fallback (str): IP to return if detection fails (default: 127.0.0.1).
        test_host (str): A dummy IP used for routing logic (default: 10.0.0.0).

    Returns:
        str: The detected local IP address.

    Note:
        This method uses a UDP socket and connect() to a non-routable IP.
        No traffic is sent — it simply triggers OS routing logic.
    """
    try:

        # https://man7.org/linux/man-pages/man2/connect.2.html
        _socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # connect() for UDP doesn't send packets
        _socket.connect((fake_address, RANDOM_PORT))
        ip, host = _socket.getsockname()

        return str(ip)
    except Exception:
        return fallback_address


if __name__ == "__main__":
    print(get_primary_local_ip())
