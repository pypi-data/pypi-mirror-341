# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class CompliantDeviceRequest:
    devices: Optional[List[str]] = _field(default=None)
    protocol_pack_name: Optional[str] = _field(default=None, metadata={"alias": "protocolPackName"})
