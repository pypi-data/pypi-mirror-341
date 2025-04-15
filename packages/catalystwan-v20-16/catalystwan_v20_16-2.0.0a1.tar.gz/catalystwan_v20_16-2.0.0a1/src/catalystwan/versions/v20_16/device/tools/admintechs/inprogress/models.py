# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class InProgressCount:
    in_progress_count: Optional[int] = _field(default=None, metadata={"alias": "inProgressCount"})
