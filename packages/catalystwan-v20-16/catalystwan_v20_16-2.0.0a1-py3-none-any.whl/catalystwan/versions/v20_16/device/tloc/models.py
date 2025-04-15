# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class DeviceTlocDataWithBfd:
    bfd_sessions_down: Optional[int] = _field(default=None, metadata={"alias": "bfdSessionsDown"})
    bfd_sessions_up: Optional[int] = _field(default=None, metadata={"alias": "bfdSessionsUp"})
    color: Optional[str] = _field(default=None)
    control_connections_down: Optional[str] = _field(
        default=None, metadata={"alias": "controlConnectionsDown"}
    )
    control_connections_up: Optional[int] = _field(
        default=None, metadata={"alias": "controlConnectionsUp"}
    )
    system_ip: Optional[str] = _field(default=None, metadata={"alias": "system-ip"})
