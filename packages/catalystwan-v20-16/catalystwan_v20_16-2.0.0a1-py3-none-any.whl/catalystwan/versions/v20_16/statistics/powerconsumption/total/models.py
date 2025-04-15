# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class PowerConsumptionTotalResp:
    change: Optional[int] = _field(default=None)
    cost: Optional[int] = _field(default=None)
    emission: Optional[int] = _field(default=None)
    power_usage: Optional[int] = _field(default=None)
