# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class DefaultSuccessResponse:
    message: Optional[str] = _field(default=None)
    success: Optional[bool] = _field(default=None)


@dataclass
class ApplicationRequestDetails:
    app_name: Optional[str] = _field(default=None, metadata={"alias": "appName"})


@dataclass
class ExtendedApplicationRequestData:
    data: Optional[List[ApplicationRequestDetails]] = _field(default=None)
    select_all: Optional[bool] = _field(default=None, metadata={"alias": "selectAll"})
