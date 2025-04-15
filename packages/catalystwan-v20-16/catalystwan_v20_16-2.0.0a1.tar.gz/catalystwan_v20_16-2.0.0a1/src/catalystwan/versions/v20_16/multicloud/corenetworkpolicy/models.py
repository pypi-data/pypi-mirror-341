# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class CoreNetworkPolicyResponse:
    change_set_state: Optional[str] = _field(default=None, metadata={"alias": "changeSetState"})
    core_network_id: Optional[str] = _field(default=None, metadata={"alias": "coreNetworkId"})
    created_at: Optional[str] = _field(default=None, metadata={"alias": "createdAt"})
    description: Optional[str] = _field(default=None)
    policy_alias: Optional[str] = _field(default=None, metadata={"alias": "policyAlias"})
    policy_data: Optional[str] = _field(default=None, metadata={"alias": "policyData"})
    policy_version_id: Optional[int] = _field(default=None, metadata={"alias": "policyVersionId"})
