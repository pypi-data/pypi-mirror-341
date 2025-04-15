# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class UserSettingsResponse:
    is_present_credentials: Optional[bool] = _field(
        default=None, metadata={"alias": "isPresentCredentials"}
    )
    # Smart Licensing mode can be 'online', 'offline' or 'onPrem'
    mode: Optional[str] = _field(default=None)
    multiple_entitlement: Optional[bool] = _field(
        default=None, metadata={"alias": "multipleEntitlement"}
    )
    # Smart Licensing user name
    uname: Optional[str] = _field(default=None)
