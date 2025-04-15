# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class Policy:
    id: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})


@dataclass
class ApplicationList:
    id: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    policies: Optional[List[Policy]] = _field(default=None)
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})


@dataclass
class Application:
    application_lists: Optional[List[ApplicationList]] = _field(
        default=None, metadata={"alias": "applicationLists"}
    )
    id: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})


@dataclass
class ApplicationRequestDetails:
    app_name: Optional[str] = _field(default=None, metadata={"alias": "appName"})


@dataclass
class ExtendedApplicationRequestData:
    data: Optional[List[ApplicationRequestDetails]] = _field(default=None)
    select_all: Optional[bool] = _field(default=None, metadata={"alias": "selectAll"})
