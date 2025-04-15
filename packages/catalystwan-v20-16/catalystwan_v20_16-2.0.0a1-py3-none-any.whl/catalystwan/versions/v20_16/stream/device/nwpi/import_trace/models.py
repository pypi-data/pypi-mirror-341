# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class ImportTraceResponse:
    msg: Optional[str] = _field(default=None)
    state: Optional[bool] = _field(default=None)


@dataclass
class ImportTraceRequest:
    file: Optional[str] = _field(default=None)
