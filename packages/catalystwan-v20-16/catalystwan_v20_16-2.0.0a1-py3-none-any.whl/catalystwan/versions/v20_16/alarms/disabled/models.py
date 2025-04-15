# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class DisabledAlarmDetails:
    end_time: Optional[str] = _field(default=None, metadata={"alias": "endTime"})
    event_name: Optional[str] = _field(default=None, metadata={"alias": "eventName"})
    start_time: Optional[str] = _field(default=None, metadata={"alias": "startTime"})
