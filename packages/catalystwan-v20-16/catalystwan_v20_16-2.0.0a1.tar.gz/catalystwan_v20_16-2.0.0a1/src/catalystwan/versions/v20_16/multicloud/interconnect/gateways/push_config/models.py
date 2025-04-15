# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class ProcessResponse:
    # Procees Id of the task
    id: Optional[str] = _field(default=None)


@dataclass
class GatewaysPushconfigBody:
    edge_gateway_name: str = _field(metadata={"alias": "edgeGatewayName"})
    edge_type: str = _field(metadata={"alias": "edgeType"})
