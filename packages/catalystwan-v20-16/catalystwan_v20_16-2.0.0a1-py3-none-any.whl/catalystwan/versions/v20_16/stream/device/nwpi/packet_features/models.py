# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class NwpipacketRespPayloadDataPacketPacketEgressFia:
    feature_detail: Optional[str] = _field(default=None)
    feature_name: Optional[str] = _field(default=None)
    fia_color: Optional[str] = _field(default=None)
    policy_key: Optional[str] = _field(default=None)


@dataclass
class NwpipacketRespPayloadDataPacketPacket:
    egress_fia: Optional[List[NwpipacketRespPayloadDataPacketPacketEgressFia]] = _field(
        default=None
    )
    ingress_fia: Optional[List[NwpipacketRespPayloadDataPacketPacketEgressFia]] = _field(
        default=None
    )


@dataclass
class NwpipacketRespPayloadDataPacket:
    app_awared: Optional[bool] = _field(default=None)
    event_name: Optional[List[str]] = _field(default=None)
    packet: Optional[NwpipacketRespPayloadDataPacketPacket] = _field(default=None)
    packet_fwd_decision: Optional[str] = _field(default=None)
    packet_id: Optional[int] = _field(default=None)
    parent_pkt_id: Optional[int] = _field(default=None)


@dataclass
class NwpipacketRespPayloadData:
    device_name: Optional[str] = _field(default=None)
    device_version: Optional[str] = _field(default=None)
    flow_id: Optional[int] = _field(default=None)
    packet: Optional[NwpipacketRespPayloadDataPacket] = _field(default=None)
    packet_received_timestamp: Optional[int] = _field(default=None)
    system_ip: Optional[str] = _field(default=None)
    trace_id: Optional[int] = _field(default=None)


@dataclass
class NwpipacketRespPayloadData1:
    data: Optional[NwpipacketRespPayloadData] = _field(default=None)
    entry_time: Optional[int] = _field(default=None)
    tenant: Optional[str] = _field(default=None)
    trace_id: Optional[int] = _field(default=None, metadata={"alias": "trace-id"})
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})


@dataclass
class NwpipacketRespPayload:
    """
    Nwpi trace packet payload schema
    """

    data: Optional[List[NwpipacketRespPayloadData1]] = _field(default=None)
