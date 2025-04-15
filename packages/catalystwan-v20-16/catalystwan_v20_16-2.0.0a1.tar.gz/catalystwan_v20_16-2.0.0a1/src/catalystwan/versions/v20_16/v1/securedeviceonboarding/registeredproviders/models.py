# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class ProviderInfo:
    cmp_type: Optional[str] = _field(default=None, metadata={"alias": "cmpType"})
    cmp_url: Optional[str] = _field(default=None, metadata={"alias": "cmpUrl"})
    contact_info_line1: Optional[str] = _field(default=None, metadata={"alias": "contactInfoLine1"})
    contact_info_line2: Optional[str] = _field(default=None, metadata={"alias": "contactInfoLine2"})
    contact_info_line3: Optional[str] = _field(default=None, metadata={"alias": "contactInfoLine3"})
    country_code: Optional[str] = _field(default=None, metadata={"alias": "countryCode"})
    operator_logo_url: Optional[str] = _field(default=None, metadata={"alias": "operatorLogoUrl"})
    operator_name: Optional[str] = _field(default=None, metadata={"alias": "operatorName"})
    terms_and_conditions: Optional[str] = _field(
        default=None, metadata={"alias": "termsAndConditions"}
    )
