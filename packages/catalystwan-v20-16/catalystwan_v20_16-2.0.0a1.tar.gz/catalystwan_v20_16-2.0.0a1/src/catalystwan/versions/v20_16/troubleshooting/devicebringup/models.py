# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

Operation = Literal[
    "ControlPlane", "DataPlane", "RouterConfiguration", "SoftwareImageUpdate", "vBondAuth"
]

Status = Literal["Error", "NA", "Success", "Unknown"]


@dataclass
class BringupInfo:
    message: Optional[List[str]] = _field(default=None)
    name: Optional[str] = _field(default=None)
    operation: Optional[Operation] = _field(default=None)
    status: Optional[Status] = _field(default=None)
    timestamp: Optional[int] = _field(default=None)


@dataclass
class GetDeviceConfiguration:
    data: Optional[List[BringupInfo]] = _field(default=None)
