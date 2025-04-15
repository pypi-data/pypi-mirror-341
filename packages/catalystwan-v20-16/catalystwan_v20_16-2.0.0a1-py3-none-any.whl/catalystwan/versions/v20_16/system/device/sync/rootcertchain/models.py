# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class SyncRootCertChain:
    sync_root_cert_chain: Optional[str] = _field(
        default=None, metadata={"alias": "syncRootCertChain"}
    )
