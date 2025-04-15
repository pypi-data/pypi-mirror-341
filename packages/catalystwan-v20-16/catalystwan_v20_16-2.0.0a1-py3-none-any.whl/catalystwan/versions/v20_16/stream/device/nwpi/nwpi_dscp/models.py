# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class NwpiDscpResponsePayloadInner:
    """
    DSCP for GET response
    """

    dscp_name: Optional[str] = _field(default=None, metadata={"alias": "dscpName"})
    value: Optional[int] = _field(default=None)
