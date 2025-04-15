# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class SecurityGroup:
    description: Optional[str] = _field(default=None)
    id: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    tag: Optional[int] = _field(default=None)


@dataclass
class SgtResponse:
    """
    Security Groups Returned from ISE
    """

    security_groups: Optional[List[SecurityGroup]] = _field(
        default=None, metadata={"alias": "securityGroups"}
    )
