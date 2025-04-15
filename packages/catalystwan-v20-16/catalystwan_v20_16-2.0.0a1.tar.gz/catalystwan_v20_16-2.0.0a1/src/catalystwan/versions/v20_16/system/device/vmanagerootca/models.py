# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class InvalidateVmanageRootCa:
    vmanage_root_ca_invalidated: Optional[str] = _field(
        default=None, metadata={"alias": "VmanageRootCAInvalidated"}
    )
