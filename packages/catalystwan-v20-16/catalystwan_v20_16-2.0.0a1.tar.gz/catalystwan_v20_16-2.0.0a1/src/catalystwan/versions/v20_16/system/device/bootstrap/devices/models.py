# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class GenerateBootstrapConfigForVedgesResponse:
    id: Optional[str] = _field(default=None)


@dataclass
class VEdgeBootstrapConfig:
    bootstrap_config_type: Optional[str] = _field(
        default=None, metadata={"alias": "bootstrapConfigType"}
    )
    uuid: Optional[List[str]] = _field(default=None)
