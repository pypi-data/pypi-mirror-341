# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

TypeParam = Literal["carrier", "product", "rat"]

LastNHoursParam = Literal["1", "12", "24", "3", "6"]


@dataclass
class CellularCount:
    active: Optional[int] = _field(default=None)
    carrier: Optional[str] = _field(default=None)
    product: Optional[str] = _field(default=None)
    rat: Optional[str] = _field(default=None)
    standby: Optional[int] = _field(default=None)
