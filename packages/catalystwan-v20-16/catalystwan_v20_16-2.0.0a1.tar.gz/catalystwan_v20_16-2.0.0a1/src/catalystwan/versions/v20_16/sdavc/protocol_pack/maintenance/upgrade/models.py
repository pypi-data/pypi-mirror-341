# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

DeviceSelectionType = Literal["entire-network", "selected-devices"]

ExecutionType = Literal["later", "now"]

ProtocolPackType = Literal[
    "built-in-protocol-pack", "default-protocol-pack", "selected-protocol-pack"
]


@dataclass
class ProtocolPackUpgradeRequest:
    device_selection_type: Optional[DeviceSelectionType] = _field(
        default=None, metadata={"alias": "deviceSelectionType"}
    )
    devices: Optional[List[str]] = _field(default=None)
    execution_type: Optional[ExecutionType] = _field(
        default=None, metadata={"alias": "executionType"}
    )
    protocol_pack_type: Optional[ProtocolPackType] = _field(
        default=None, metadata={"alias": "protocolPackType"}
    )
    protocol_packs: Optional[List[str]] = _field(default=None, metadata={"alias": "protocolPacks"})
    schedule_time: Optional[int] = _field(default=None, metadata={"alias": "scheduleTime"})
