# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class DeviceIp:
    """
    This is the valid DeviceIP
    """

    device_ip: Optional[str] = _field(default=None, metadata={"alias": "deviceIp"})


@dataclass
class TaskId:
    id: Optional[str] = _field(default=None)
