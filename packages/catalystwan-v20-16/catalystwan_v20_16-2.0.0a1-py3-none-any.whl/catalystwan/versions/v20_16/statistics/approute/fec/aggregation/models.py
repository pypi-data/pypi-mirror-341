# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class AppRouteFecAggRespInner:
    count: Optional[int] = _field(default=None)
    entry_time: Optional[str] = _field(default=None)
    fec_loss_recovery: Optional[str] = _field(default=None, metadata={"alias": "fecLossRecovery"})
    loss_percentage: Optional[int] = _field(default=None)
    name: Optional[str] = _field(default=None)
    proto: Optional[str] = _field(default=None)
    state: Optional[str] = _field(default=None)
