# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class LicenseInfo:
    available: Optional[str] = _field(default=None, metadata={"alias": "Available"})
    billing_model: Optional[str] = _field(default=None)
    billing_type: Optional[str] = _field(default=None)
    display_name: Optional[str] = _field(default=None)
    in_use: Optional[str] = _field(default=None, metadata={"alias": "inUse"})
    purchased: Optional[int] = _field(default=None, metadata={"alias": "Purchased"})
    quantity: Optional[str] = _field(default=None)
    tag: Optional[str] = _field(default=None)


@dataclass
class GetLicenseResponseInner:
    billing_model: Optional[str] = _field(default=None)
    billing_type: Optional[str] = _field(default=None)
    licenses: Optional[List[LicenseInfo]] = _field(default=None)
    subscription_id: Optional[str] = _field(default=None)
