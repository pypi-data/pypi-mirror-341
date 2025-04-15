# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class FecAndPktDupResponseHeader:
    columns: Optional[List[str]] = _field(default=None)
    fields: Optional[List[str]] = _field(default=None)
    generated_on: Optional[int] = _field(default=None, metadata={"alias": "generatedOn"})


@dataclass
class FecAndPktDupResponse:
    data: Optional[List[str]] = _field(default=None)
    header: Optional[FecAndPktDupResponseHeader] = _field(default=None)
