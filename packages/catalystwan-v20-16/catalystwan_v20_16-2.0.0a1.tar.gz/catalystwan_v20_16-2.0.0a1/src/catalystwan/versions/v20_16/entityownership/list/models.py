# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class EntityOwnershipInfo:
    bucket: Optional[str] = _field(default=None)
    entity_name: Optional[str] = _field(default=None, metadata={"alias": "entityName"})
    owner: Optional[str] = _field(default=None)
