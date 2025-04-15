# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Optional


@dataclass
class EventAppHopListResponsePayloadInner:
    """
    Application and HopList schema for GET response
    """

    application: Optional[str] = _field(default=None)
    down_hop_list_info: Optional[List[Any]] = _field(
        default=None, metadata={"alias": "downHopListInfo"}
    )
    down_max_hop_num: Optional[int] = _field(default=None, metadata={"alias": "downMaxHopNum"})
    entry_time: Optional[int] = _field(default=None)
    server_side_key: Optional[str] = _field(default=None, metadata={"alias": "serverSideKey"})
    trace_id: Optional[int] = _field(default=None)
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})
    up_hop_list_info: Optional[List[Any]] = _field(
        default=None, metadata={"alias": "upHopListInfo"}
    )
    up_max_hop_num: Optional[int] = _field(default=None, metadata={"alias": "upMaxHopNum"})
    vpn_id: Optional[str] = _field(default=None)
