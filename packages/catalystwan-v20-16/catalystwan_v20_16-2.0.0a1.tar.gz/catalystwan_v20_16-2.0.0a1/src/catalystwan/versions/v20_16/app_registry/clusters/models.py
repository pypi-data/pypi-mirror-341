# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class ClusterProperties:
    account_id: Optional[str] = _field(default=None, metadata={"alias": "accountId"})
    account_name: Optional[str] = _field(default=None, metadata={"alias": "accountName"})
    account_type: Optional[str] = _field(default=None, metadata={"alias": "accountType"})
    discovery_status: Optional[bool] = _field(default=None, metadata={"alias": "discoveryStatus"})
    expiration: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class PutProperties:
    discovery_status: Optional[bool] = _field(default=None, metadata={"alias": "discoveryStatus"})
