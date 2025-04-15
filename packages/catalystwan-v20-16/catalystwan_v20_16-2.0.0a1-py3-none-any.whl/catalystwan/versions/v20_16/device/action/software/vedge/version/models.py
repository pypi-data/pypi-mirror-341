# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class FindVEdgeSoftwareVersionData:
    version: Optional[str] = _field(default=None)
    version_id: Optional[str] = _field(default=None, metadata={"alias": "versionId"})


@dataclass
class FindVEdgeSoftwareVersion:
    data: Optional[List[FindVEdgeSoftwareVersionData]] = _field(default=None)
