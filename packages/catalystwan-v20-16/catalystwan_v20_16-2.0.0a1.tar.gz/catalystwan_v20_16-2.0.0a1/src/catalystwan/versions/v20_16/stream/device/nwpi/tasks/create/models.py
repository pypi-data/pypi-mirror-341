# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class TasksCreateResponsePayload:
    """
    Auto on task create schema for POST response
    """

    action: Optional[str] = _field(default=None)
    entry_time: Optional[int] = _field(default=None)
    expire_time: Optional[int] = _field(default=None, metadata={"alias": "expire-time"})
    sites: Optional[List[str]] = _field(default=None)
    state: Optional[str] = _field(default=None)
    task_id: Optional[int] = _field(default=None, metadata={"alias": "taskId"})
    task_name: Optional[str] = _field(default=None, metadata={"alias": "taskName"})
