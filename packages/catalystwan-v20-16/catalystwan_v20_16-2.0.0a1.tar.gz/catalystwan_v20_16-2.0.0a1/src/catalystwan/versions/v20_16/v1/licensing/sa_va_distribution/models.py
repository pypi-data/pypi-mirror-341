# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class SaVaDistributionResponseSaVaMap:
    allocated: Optional[int] = _field(default=None)
    available: Optional[int] = _field(default=None)
    in_use: Optional[int] = _field(default=None, metadata={"alias": "inUse"})
    sa_name: Optional[str] = _field(default=None, metadata={"alias": "saName"})
    subscription_id: Optional[str] = _field(default=None, metadata={"alias": "subscriptionId"})
    va_name: Optional[str] = _field(default=None, metadata={"alias": "vaName"})


@dataclass
class SaVaDistributionResponseBaseLicenses:
    display_name: Optional[str] = _field(default=None, metadata={"alias": "displayName"})
    platform_class: Optional[str] = _field(default=None, metadata={"alias": "platformClass"})
    sava_map: Optional[List[SaVaDistributionResponseSaVaMap]] = _field(
        default=None, metadata={"alias": "savaMap"}
    )
    tag: Optional[str] = _field(default=None)
    # List of device UUIDs
    uuids: Optional[List[str]] = _field(default=None)


@dataclass
class SaVaDistributionResponseTenantLicenses:
    display_name: Optional[str] = _field(default=None, metadata={"alias": "displayName"})
    sava_map: Optional[List[SaVaDistributionResponseSaVaMap]] = _field(
        default=None, metadata={"alias": "savaMap"}
    )
    tag: Optional[str] = _field(default=None)


@dataclass
class SaVaDistributionResponse:
    base_licenses: Optional[List[SaVaDistributionResponseBaseLicenses]] = _field(
        default=None, metadata={"alias": "baseLicenses"}
    )
    tenant_licenses: Optional[SaVaDistributionResponseTenantLicenses] = _field(
        default=None, metadata={"alias": "tenantLicenses"}
    )


@dataclass
class AppliedFilters:
    billing_type: Optional[str] = _field(default=None, metadata={"alias": "billingType"})
    license_classification: Optional[str] = _field(
        default=None, metadata={"alias": "licenseClassification"}
    )


@dataclass
class SaVaDistributionRequestBaseLicenses:
    display_name: Optional[str] = _field(default=None, metadata={"alias": "displayName"})
    platform_class: Optional[str] = _field(default=None, metadata={"alias": "platformClass"})
    tag: Optional[str] = _field(default=None)
    # List of device UUIDs
    uuids: Optional[List[str]] = _field(default=None)


@dataclass
class SaVaDistributionRequestTenantLicense:
    display_name: Optional[str] = _field(default=None, metadata={"alias": "displayName"})
    tag: Optional[str] = _field(default=None)
    total_tenant_lic_required: Optional[int] = _field(
        default=None, metadata={"alias": "totalTenantLicRequired"}
    )


@dataclass
class SaVaDistributionRequest:
    applied_filters: Optional[AppliedFilters] = _field(
        default=None, metadata={"alias": "appliedFilters"}
    )
    base_licenses: Optional[List[SaVaDistributionRequestBaseLicenses]] = _field(
        default=None, metadata={"alias": "baseLicenses"}
    )
    tenant_licenses: Optional[SaVaDistributionRequestTenantLicense] = _field(
        default=None, metadata={"alias": "tenantLicenses"}
    )
