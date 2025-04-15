# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class DeleteResponseInner:
    host: Optional[str] = _field(default=None)
    reason: Optional[str] = _field(default=None)


@dataclass
class DeleteDetails:
    devices: Optional[List[str]] = _field(default=None)
