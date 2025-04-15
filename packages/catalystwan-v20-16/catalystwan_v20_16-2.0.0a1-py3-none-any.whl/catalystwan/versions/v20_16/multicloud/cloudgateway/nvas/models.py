# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class NvasResponse:
    nva_id: Optional[str] = _field(default=None, metadata={"alias": "nvaId"})
    nva_name: Optional[str] = _field(default=None, metadata={"alias": "nvaName"})
    source: Optional[str] = _field(default=None)
    uuids: Optional[List[str]] = _field(default=None)
