# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class Taskid:
    """
    Task id for polling status
    """

    id: Optional[str] = _field(default=None)


@dataclass
class TelemetryRequests:
    cloud_type: str = _field(metadata={"alias": "cloudType"})
    cgw_list: Optional[List[str]] = _field(default=None, metadata={"alias": "cgwList"})
