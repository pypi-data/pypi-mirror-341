# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class PurgeFrequency:
    active_time: Optional[str] = _field(default=None, metadata={"alias": "activeTime"})
    interval: Optional[str] = _field(default=None)
