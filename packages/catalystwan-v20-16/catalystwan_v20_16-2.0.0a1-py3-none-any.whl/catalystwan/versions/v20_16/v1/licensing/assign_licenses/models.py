# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class AssignLicensesRequestAssignLicenses:
    allocated: Optional[int] = _field(default=None)
    billing_type: Optional[str] = _field(default=None, metadata={"alias": "billingType"})
    display_name: Optional[str] = _field(default=None, metadata={"alias": "displayName"})
    sa_name: Optional[str] = _field(default=None, metadata={"alias": "saName"})
    subscription_id: Optional[str] = _field(default=None, metadata={"alias": "subscriptionId"})
    tag: Optional[str] = _field(default=None)
    va_name: Optional[str] = _field(default=None, metadata={"alias": "vaName"})


@dataclass
class AssignLicensesRequestBaseLicenses:
    assign_licenses: Optional[List[AssignLicensesRequestAssignLicenses]] = _field(
        default=None, metadata={"alias": "assignLicenses"}
    )
    # List of device UUIDs
    uuids: Optional[List[str]] = _field(default=None)


@dataclass
class AssignLicensesRequest:
    base_licenses: Optional[List[AssignLicensesRequestBaseLicenses]] = _field(
        default=None, metadata={"alias": "baseLicenses"}
    )
    tenant_licenses: Optional[List[AssignLicensesRequestAssignLicenses]] = _field(
        default=None, metadata={"alias": "tenantLicenses"}
    )
