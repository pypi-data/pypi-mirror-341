import os


SUDO_USER_GUID = 0
SUDO_USER_ENV = "SUDO_USER"


def check_if_admin() -> None:
    if SUDO_USER_ENV not in os.environ and os.getuid() != 0:
        raise Exception("Need admin priviliges")
