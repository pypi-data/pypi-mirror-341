# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class AdminTechsUploadReq:
    request_token_id: Optional[str] = _field(default=None, metadata={"alias": "requestTokenId"})
    sr_number: Optional[str] = _field(default=None)
    token: Optional[str] = _field(default=None)
    vpn: Optional[str] = _field(default=None)
