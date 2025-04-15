# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

TypeParam = Literal["carrier", "rat"]

LastNHoursParam = Literal["1", "12", "24", "3", "6"]


@dataclass
class CellularHealth:
    carrier: Optional[str] = _field(default=None)
    excellent: Optional[int] = _field(default=None)
    fair: Optional[int] = _field(default=None)
    good: Optional[int] = _field(default=None)
    poor: Optional[int] = _field(default=None)
    rat: Optional[str] = _field(default=None)
