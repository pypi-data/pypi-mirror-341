# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class LicensesResponseLicenses:
    available: Optional[int] = _field(default=None)
    display_name: Optional[str] = _field(default=None, metadata={"alias": "displayName"})
    in_use: Optional[int] = _field(default=None, metadata={"alias": "inUse"})
    is_preferred: Optional[bool] = _field(default=None, metadata={"alias": "isPreferred"})
    tag: Optional[str] = _field(default=None)


@dataclass
class LicensesResponseBaseLicenses:
    licenses: Optional[List[LicensesResponseLicenses]] = _field(default=None)
    platform_class: Optional[str] = _field(default=None, metadata={"alias": "platformClass"})
    # List of device UUIDs
    uuids: Optional[List[str]] = _field(default=None)


@dataclass
class LicensesResponseTenantLicenses:
    licenses: Optional[List[LicensesResponseLicenses]] = _field(default=None)
    total_tenant_lic_required: Optional[int] = _field(
        default=None, metadata={"alias": "totalTenantLicRequired"}
    )


@dataclass
class LicensesResponse:
    base_licenses: Optional[List[LicensesResponseBaseLicenses]] = _field(
        default=None, metadata={"alias": "baseLicenses"}
    )
    tenant_licenses: Optional[LicensesResponseTenantLicenses] = _field(
        default=None, metadata={"alias": "tenantLicenses"}
    )


@dataclass
class AppliedFilters:
    billing_type: Optional[str] = _field(default=None, metadata={"alias": "billingType"})
    license_classification: Optional[str] = _field(
        default=None, metadata={"alias": "licenseClassification"}
    )


@dataclass
class LicensesRequest:
    applied_filters: Optional[AppliedFilters] = _field(
        default=None, metadata={"alias": "appliedFilters"}
    )
    # List of device UUIDs
    uuids: Optional[List[str]] = _field(default=None)
