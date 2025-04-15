# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class DeleteAllListsBody:
    """
    Body for deleteAllLists call, generic api for deleting all lists of a specified listType
    """

    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})
