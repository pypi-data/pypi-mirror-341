# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class Entry:
    """
    list
    """

    user_group: Optional[str] = _field(default=None, metadata={"alias": "userGroup"})


@dataclass
class Reference:
    """
    single policy where list is referenced
    """

    id: Optional[str] = _field(default=None)
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})


@dataclass
class ReferencedList:
    """
    A single list and where it is referenced
    """

    description: Optional[str] = _field(default=None)
    entries: Optional[List[Entry]] = _field(default=None)
    info_tag: Optional[str] = _field(default=None, metadata={"alias": "infoTag"})
    is_activated_by_vsmart: Optional[bool] = _field(
        default=None, metadata={"alias": "isActivatedByVsmart"}
    )
    last_updated: Optional[int] = _field(default=None, metadata={"alias": "lastUpdated"})
    list_id: Optional[str] = _field(default=None, metadata={"alias": "listId"})
    name: Optional[str] = _field(default=None)
    owner: Optional[str] = _field(default=None)
    read_only: Optional[bool] = _field(default=None, metadata={"alias": "readOnly"})
    reference_count: Optional[int] = _field(default=None, metadata={"alias": "referenceCount"})
    references: Optional[List[Reference]] = _field(default=None)
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})
    version: Optional[str] = _field(default=None)
