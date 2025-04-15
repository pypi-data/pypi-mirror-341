# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class RadiusServer:
    host: str
    port: int
    secret: str


@dataclass
class Radius:
    retransmit: Optional[int] = _field(default=None)
    server: Optional[List[RadiusServer]] = _field(default=None)
    timeout: Optional[int] = _field(default=None)
