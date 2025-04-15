# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class PowerConsumptionBreakDown:
    percentage: Optional[int] = _field(default=None)
    property: Optional[str] = _field(default=None)
    usage: Optional[int] = _field(default=None)


@dataclass
class PowerConsumptionEnergyMixResp:
    energy_mix: Optional[List[PowerConsumptionBreakDown]] = _field(
        default=None, metadata={"alias": "energyMix"}
    )
    low_carbon: Optional[int] = _field(default=None)
