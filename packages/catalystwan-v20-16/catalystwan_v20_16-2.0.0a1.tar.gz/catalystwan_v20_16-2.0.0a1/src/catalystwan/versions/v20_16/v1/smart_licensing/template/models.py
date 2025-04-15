# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class SaveTemplateRequestLicenseTemplateLicenses:
    display_name: Optional[str] = _field(default=None)
    tag: Optional[str] = _field(default=None)


@dataclass
class SaveTemplateRequestLicenseTemplateSubscriptionsUsed:
    subscription_id: Optional[str] = _field(default=None)


@dataclass
class SaveTemplateRequestLicenseTemplate:
    license_type: Optional[str] = _field(default=None, metadata={"alias": "licenseType"})
    licenses: Optional[List[SaveTemplateRequestLicenseTemplateLicenses]] = _field(default=None)
    sa_account: Optional[str] = _field(default=None, metadata={"alias": "saAccount"})
    sa_name: Optional[str] = _field(default=None, metadata={"alias": "saName"})
    subscriptions_used: Optional[List[SaveTemplateRequestLicenseTemplateSubscriptionsUsed]] = (
        _field(default=None, metadata={"alias": "subscriptionsUsed"})
    )
    template_name: Optional[str] = _field(default=None, metadata={"alias": "templateName"})
    use_existing_template: Optional[bool] = _field(
        default=None, metadata={"alias": "useExistingTemplate"}
    )
    uuid: Optional[List[str]] = _field(default=None)
    va_account: Optional[str] = _field(default=None, metadata={"alias": "vaAccount"})
    va_name: Optional[str] = _field(default=None, metadata={"alias": "vaName"})


@dataclass
class SaveTemplateRequest:
    license_template: Optional[SaveTemplateRequestLicenseTemplate] = _field(
        default=None, metadata={"alias": "licenseTemplate"}
    )
