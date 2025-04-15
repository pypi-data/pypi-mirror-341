# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class DeviceBlistDeleteResponsePayload:
    """
    Device blist delete response schema
    """

    action: Optional[str] = _field(default=None)
    message: Optional[str] = _field(default=None)
