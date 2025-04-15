# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class InlineResponse2002:
    loopback_cgw_color: Optional[List[str]] = _field(
        default=None, metadata={"alias": "loopbackCgwColor"}
    )
    loopback_tunnel_color: Optional[List[str]] = _field(
        default=None, metadata={"alias": "loopbackTunnelColor"}
    )
