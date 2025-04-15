# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class EventReadoutsResponsePayloadDropSendPkts:
    drop_pkts: Optional[int] = _field(default=None, metadata={"alias": "dropPkts"})
    event: Optional[str] = _field(default=None)
    send_pkts: Optional[int] = _field(default=None, metadata={"alias": "sendPkts"})


@dataclass
class EventReadoutsResponsePayloadTimeInfo:
    end_time: Optional[str] = _field(default=None, metadata={"alias": "endTime"})
    event_num: Optional[str] = _field(default=None, metadata={"alias": "eventNum"})
    start_time: Optional[str] = _field(default=None, metadata={"alias": "startTime"})


@dataclass
class EventReadoutsResponsePayloadEventHopTimeInfo:
    event_hop: Optional[str] = _field(default=None, metadata={"alias": "eventHop"})
    event_hop_with_edge: Optional[str] = _field(
        default=None, metadata={"alias": "eventHopWithEdge"}
    )
    time_info: Optional[List[EventReadoutsResponsePayloadTimeInfo]] = _field(
        default=None, metadata={"alias": "timeInfo"}
    )


@dataclass
class EventReadoutsResponsePayloadDropCauses:
    drop_cause: Optional[str] = _field(default=None, metadata={"alias": "dropCause"})


@dataclass
class EventReadoutsResponsePayloadHopStatistics:
    drop_causes: Optional[List[EventReadoutsResponsePayloadDropCauses]] = _field(
        default=None, metadata={"alias": "dropCauses"}
    )
    event_num: Optional[str] = _field(default=None, metadata={"alias": "eventNum"})
    hop: Optional[str] = _field(default=None)
    hop_with_edge: Optional[str] = _field(default=None, metadata={"alias": "hopWithEdge"})


@dataclass
class EventReadoutsResponsePayloadEventHopStatistics:
    event: Optional[str] = _field(default=None)
    hop_statistics: Optional[List[EventReadoutsResponsePayloadHopStatistics]] = _field(
        default=None, metadata={"alias": "hopStatistics"}
    )


@dataclass
class EventReadoutsResponsePayloadEventImpactedFlowNum:
    event: Optional[str] = _field(default=None)
    impacted_flow_num: Optional[str] = _field(default=None, metadata={"alias": "impactedFlowNum"})


@dataclass
class EventReadoutsResponsePayloadEventNum:
    event: Optional[str] = _field(default=None)
    event_num: Optional[str] = _field(default=None, metadata={"alias": "eventNum"})


@dataclass
class EventReadoutsResponsePayloadDetail:
    application: Optional[str] = _field(default=None)
    drop_send_pkts: Optional[List[EventReadoutsResponsePayloadDropSendPkts]] = _field(
        default=None, metadata={"alias": "dropSendPkts"}
    )
    event_hop_policy_info: Optional[List[EventReadoutsResponsePayloadEventHopTimeInfo]] = _field(
        default=None, metadata={"alias": "eventHopPolicyInfo"}
    )
    event_hop_statistics: Optional[List[EventReadoutsResponsePayloadEventHopStatistics]] = _field(
        default=None, metadata={"alias": "eventHopStatistics"}
    )
    event_hop_time_info: Optional[List[EventReadoutsResponsePayloadEventHopTimeInfo]] = _field(
        default=None, metadata={"alias": "eventHopTimeInfo"}
    )
    event_impacted_flow_num: Optional[List[EventReadoutsResponsePayloadEventImpactedFlowNum]] = (
        _field(default=None, metadata={"alias": "eventImpactedFlowNum"})
    )
    event_list: Optional[List[str]] = _field(default=None, metadata={"alias": "eventList"})
    event_num: Optional[List[EventReadoutsResponsePayloadEventNum]] = _field(
        default=None, metadata={"alias": "eventNum"}
    )
    total_flow_num: Optional[int] = _field(default=None, metadata={"alias": "totalFlowNum"})


@dataclass
class EventReadoutsResponsePayloadData:
    app: Optional[str] = _field(default=None)
    app_grp: Optional[str] = _field(default=None)
    app_vis: Optional[str] = _field(default=None)
    art_vis: Optional[str] = _field(default=None)
    common_app: Optional[str] = _field(default=None)
    detail: Optional[List[EventReadoutsResponsePayloadDetail]] = _field(default=None)
    device_ip: Optional[str] = _field(default=None)
    dia_vis: Optional[str] = _field(default=None)
    domain_mon: Optional[str] = _field(default=None)
    dscp: Optional[str] = _field(default=None)
    dst_ip: Optional[str] = _field(default=None)
    dst_pfx: Optional[str] = _field(default=None)
    dst_pfx_len: Optional[str] = _field(default=None)
    dst_port: Optional[str] = _field(default=None)
    duration: Optional[str] = _field(default=None)
    entry_time: Optional[int] = _field(default=None)
    hub_wan_vis: Optional[str] = _field(default=None)
    local_drop_rate_threshold: Optional[int] = _field(default=None)
    message: Optional[str] = _field(default=None)
    protocol: Optional[str] = _field(default=None)
    qos_mon: Optional[str] = _field(default=None)
    sampling: Optional[str] = _field(default=None)
    source_site: Optional[str] = _field(default=None)
    source_site_vmanage_version: Optional[str] = _field(default=None)
    spl_intvl: Optional[str] = _field(default=None)
    src_if: Optional[str] = _field(default=None)
    src_ip: Optional[str] = _field(default=None)
    src_pfx: Optional[str] = _field(default=None)
    src_pfx_len: Optional[str] = _field(default=None)
    src_port: Optional[str] = _field(default=None)
    state: Optional[str] = _field(default=None)
    stop_time: Optional[int] = _field(default=None)
    trace_id: Optional[int] = _field(default=None)
    trace_name: Optional[str] = _field(default=None)
    vpn_id: Optional[str] = _field(default=None)
    wan_drop_rate_threshold: Optional[int] = _field(default=None)
    warning: Optional[str] = _field(default=None)
