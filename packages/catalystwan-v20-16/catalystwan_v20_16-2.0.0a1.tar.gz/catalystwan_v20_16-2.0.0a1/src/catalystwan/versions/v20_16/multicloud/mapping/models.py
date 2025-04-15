# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class CgwVpnsResponse:
    account_name: Optional[str] = _field(default=None, metadata={"alias": "accountName"})
    host_vpc_id: Optional[str] = _field(default=None, metadata={"alias": "hostVpcId"})
    # Returned for AWS/AWS_GOVCLOUD/GCP
    host_vpc_name: Optional[str] = _field(default=None, metadata={"alias": "hostVpcName"})
    tag: Optional[str] = _field(default=None)
    # Returned for AWS/AWS_GOVCLOUD/GCP
    tunnel_count: Optional[int] = _field(default=None, metadata={"alias": "tunnelCount"})
    vpn_id: Optional[str] = _field(default=None, metadata={"alias": "vpnId"})
