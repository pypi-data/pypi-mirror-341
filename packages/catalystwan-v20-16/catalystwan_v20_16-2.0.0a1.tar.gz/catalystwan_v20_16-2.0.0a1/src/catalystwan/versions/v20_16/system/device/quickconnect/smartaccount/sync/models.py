# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class SyncDevicesResp:
    process_id: Optional[str] = _field(default=None, metadata={"alias": "processId"})


@dataclass
class SmartAccountModel:
    client_credentials: Optional[bool] = _field(
        default=None, metadata={"alias": "clientCredentials"}
    )
    env: Optional[str] = _field(default=None)
    organization_name: Optional[str] = _field(default=None)
    password: Optional[str] = _field(default=None)
    username: Optional[str] = _field(default=None)
    validity_string: Optional[str] = _field(default=None)
