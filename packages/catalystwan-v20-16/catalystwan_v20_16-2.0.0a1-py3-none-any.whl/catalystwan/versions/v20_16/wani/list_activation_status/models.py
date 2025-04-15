# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class ActivationStatusRes:
    centralized_policy_active: bool = _field(metadata={"alias": "centralizedPolicyActive"})
    is_activated_by_v_smarts: bool = _field(metadata={"alias": "isActivatedByVSmarts"})
    activated_centralized_policy_id: Optional[str] = _field(
        default=None, metadata={"alias": "activatedCentralizedPolicyId"}
    )
    referred_in_active_wani_policy: Optional[bool] = _field(
        default=None, metadata={"alias": "referredInActiveWaniPolicy"}
    )
    user_defined_policy_id: Optional[str] = _field(
        default=None, metadata={"alias": "userDefinedPolicyId"}
    )
