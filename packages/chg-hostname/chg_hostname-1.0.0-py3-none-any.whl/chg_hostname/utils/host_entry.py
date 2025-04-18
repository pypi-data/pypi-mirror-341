from typing import Annotated, List
from pydantic import BaseModel, Field, IPvAnyAddress, StringConstraints

from chg_hostname.utils.get_ip import get_primary_local_ip

DomainName = Annotated[
    str,
    StringConstraints(
        pattern=r"^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    ),
]


class HostRecord(BaseModel):
    hostname: DomainName
    ip: IPvAnyAddress

    model_config = {
        "extra": "forbid",
        "populate_by_name": True,
        "str_strip_whitespace": True,
    }


class NetworkConfig(BaseModel):
    loopback_ip: IPvAnyAddress = Field(
        default_factory=lambda: get_primary_local_ip(), validate_default=True
    )
    host_entries: List[HostRecord]
