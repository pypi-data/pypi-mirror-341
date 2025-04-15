# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class StatusObject:
    count: Optional[int] = _field(default=None)
    message: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    status: Optional[str] = _field(default=None)


@dataclass
class DeviceStatusData:
    count: Optional[int] = _field(default=None)
    details_url: Optional[str] = _field(default=None, metadata={"alias": "detailsURL"})
    image: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    status_list: Optional[List[StatusObject]] = _field(
        default=None, metadata={"alias": "statusList"}
    )
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})
