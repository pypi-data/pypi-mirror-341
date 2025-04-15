# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class AppliedFilters:
    billing_type: Optional[str] = _field(default=None, metadata={"alias": "billingType"})
    license_classification: Optional[str] = _field(
        default=None, metadata={"alias": "licenseClassification"}
    )


@dataclass
class EditLicenseResponseLicenses:
    available: Optional[int] = _field(default=None)
    display_name: Optional[str] = _field(default=None, metadata={"alias": "displayName"})
    in_use: Optional[int] = _field(default=None, metadata={"alias": "inUse"})
    is_assigned: Optional[bool] = _field(default=None, metadata={"alias": "isAssigned"})
    tag: Optional[str] = _field(default=None)


@dataclass
class EditLicenseResponseBaseLicenses:
    licenses: Optional[List[EditLicenseResponseLicenses]] = _field(default=None)
    platform_class: Optional[str] = _field(default=None, metadata={"alias": "platformClass"})


@dataclass
class EditLicenseResponseTenantLicenses:
    licenses: Optional[List[EditLicenseResponseLicenses]] = _field(default=None)
    total_tenant_lic_required: Optional[int] = _field(
        default=None, metadata={"alias": "totalTenantLicRequired"}
    )


@dataclass
class EditLicenseResponse:
    applied_filters: Optional[AppliedFilters] = _field(
        default=None, metadata={"alias": "appliedFilters"}
    )
    base_licenses: Optional[EditLicenseResponseBaseLicenses] = _field(
        default=None, metadata={"alias": "baseLicenses"}
    )
    tenant_licenses: Optional[EditLicenseResponseTenantLicenses] = _field(
        default=None, metadata={"alias": "tenantLicenses"}
    )
