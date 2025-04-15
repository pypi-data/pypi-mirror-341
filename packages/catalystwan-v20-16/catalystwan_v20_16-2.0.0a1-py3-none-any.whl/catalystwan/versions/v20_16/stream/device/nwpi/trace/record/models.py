# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class NwpiResponsePayload:
    """
    Nwpi common response payload schema
    """

    status: Optional[str] = _field(default=None)
