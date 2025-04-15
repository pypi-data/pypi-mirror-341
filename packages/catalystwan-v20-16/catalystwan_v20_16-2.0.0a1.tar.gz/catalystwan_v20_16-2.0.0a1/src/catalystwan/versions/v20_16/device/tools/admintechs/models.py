# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class AdminTechsRes:
    creation_time: Optional[int] = _field(default=None, metadata={"alias": "creationTime"})
    device_ip: Optional[str] = _field(default=None, metadata={"alias": "deviceIP"})
    file_name: Optional[str] = _field(default=None, metadata={"alias": "fileName"})
    local_system_ip: Optional[str] = _field(default=None, metadata={"alias": "local-system-ip"})
    request_token_id: Optional[str] = _field(default=None, metadata={"alias": "requestTokenId"})
    size: Optional[int] = _field(default=None)
    state: Optional[str] = _field(default=None)
    tac_state: Optional[str] = _field(default=None)
