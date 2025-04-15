# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class AppListDetails:
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    id: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})
    version: Optional[str] = _field(default=None)


@dataclass
class PolicyComplianceApplications:
    new_applications: Optional[List[str]] = _field(
        default=None, metadata={"alias": "newApplications"}
    )
    old_applications: Optional[List[str]] = _field(
        default=None, metadata={"alias": "oldApplications"}
    )


@dataclass
class PolicyDetails:
    id: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})
    version: Optional[str] = _field(default=None)


@dataclass
class PolicyComplianceDetails:
    app_list: Optional[AppListDetails] = _field(default=None, metadata={"alias": "appList"})
    applications: Optional[List[PolicyComplianceApplications]] = _field(default=None)
    policy: Optional[List[PolicyDetails]] = _field(default=None)


@dataclass
class PolicyComplianceResponse:
    count: Optional[int] = _field(default=None)
    data: Optional[List[PolicyComplianceDetails]] = _field(default=None)


@dataclass
class ApplicationRequestDetails:
    app_name: Optional[str] = _field(default=None, metadata={"alias": "appName"})


@dataclass
class ExtendedApplicationRequestData:
    data: Optional[List[ApplicationRequestDetails]] = _field(default=None)
    select_all: Optional[bool] = _field(default=None, metadata={"alias": "selectAll"})
