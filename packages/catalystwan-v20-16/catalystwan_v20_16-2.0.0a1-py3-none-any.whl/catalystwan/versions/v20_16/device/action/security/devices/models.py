# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

PolicyTypeParam = Literal[
    "advancedMalwareProtection",
    "dnsSecurity",
    "intrusionPrevention",
    "sslDecryption",
    "urlFiltering",
    "zoneBasedFW",
]


@dataclass
class GroupId:
    """
    This is the valid GroupId
    """

    group_id: Optional[str] = _field(default=None, metadata={"alias": "groupId"})
