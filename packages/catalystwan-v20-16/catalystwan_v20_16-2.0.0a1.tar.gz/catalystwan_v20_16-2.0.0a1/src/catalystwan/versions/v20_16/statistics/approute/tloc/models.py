# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class AppRouteTlocRespInner:
    count: Optional[int] = _field(default=None)
    local_tloc: Optional[str] = _field(default=None)
    rx_octets: Optional[int] = _field(default=None)
    siteid: Optional[str] = _field(default=None)
    tx_octets: Optional[int] = _field(default=None)
