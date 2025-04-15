# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class NwpitraceFlowRespPayloadDataDownstreamDeviceList:
    device_name: Optional[str] = _field(default=None)
    device_system_ip: Optional[str] = _field(default=None)
    down_fwd_decision: Optional[str] = _field(default=None)
    egress_next_invalid: Optional[bool] = _field(default=None)
    local_color: Optional[str] = _field(default=None, metadata={"alias": "localColor"})
    remote_color: Optional[str] = _field(default=None, metadata={"alias": "remoteColor"})
    up_fwd_decision: Optional[str] = _field(default=None)


@dataclass
class NwpitraceFlowRespPayloadDataDownstreamHopList:
    appqoe_diverted: Optional[bool] = _field(default=None)
    art: Optional[str] = _field(default=None)
    asymmetry_detected: Optional[bool] = _field(default=None)
    big_drop: Optional[bool] = _field(default=None)
    big_wan_drop: Optional[bool] = _field(default=None)
    dpi_policy_used: Optional[bool] = _field(default=None)
    fif_dpi_not_classified: Optional[bool] = _field(default=None)
    flow_id: Optional[int] = _field(default=None)
    his_q_d_avg_pkts: Optional[int] = _field(default=None)
    his_q_d_max_pkts: Optional[int] = _field(default=None)
    his_q_d_min_pkts: Optional[int] = _field(default=None)
    hop_index: Optional[int] = _field(default=None)
    jitter: Optional[str] = _field(default=None)
    latency: Optional[str] = _field(default=None)
    local_color: Optional[str] = _field(default=None)
    local_drop_cause_num: Optional[int] = _field(default=None)
    local_drop_rate: Optional[str] = _field(default=None)
    local_edge: Optional[str] = _field(default=None)
    local_system_ip: Optional[str] = _field(default=None)
    nat_translated: Optional[bool] = _field(default=None)
    path_changed: Optional[bool] = _field(default=None)
    policy_bypassed: Optional[bool] = _field(default=None)
    q_d_avg_pkts: Optional[int] = _field(default=None)
    q_d_max_pkts: Optional[int] = _field(default=None)
    q_d_min_pkts: Optional[int] = _field(default=None)
    q_id: Optional[int] = _field(default=None)
    q_lim_pkts: Optional[int] = _field(default=None)
    qos_congested: Optional[bool] = _field(default=None)
    remote_color: Optional[str] = _field(default=None)
    remote_drop_cause_num: Optional[int] = _field(default=None)
    remote_drop_rate: Optional[str] = _field(default=None)
    remote_edge: Optional[str] = _field(default=None)
    remote_system_ip: Optional[str] = _field(default=None)
    server_no_response: Optional[bool] = _field(default=None)
    sla_violated: Optional[bool] = _field(default=None)
    sla_violated_bfd: Optional[bool] = _field(default=None)
    tcp_flow_reset: Optional[bool] = _field(default=None)
    total_bytes: Optional[str] = _field(default=None)
    total_packets: Optional[str] = _field(default=None)
    utd_diverted: Optional[bool] = _field(default=None)
    wan_color_asym: Optional[bool] = _field(default=None)
    wan_drop_rate: Optional[str] = _field(default=None)
    wan_drop_str: Optional[str] = _field(default=None)


@dataclass
class NwpitraceFlowRespPayloadDataFlowReadout:
    application: Optional[str] = _field(default=None)
    flow_last_update_time: Optional[str] = _field(
        default=None, metadata={"alias": "flowLastUpdateTime"}
    )
    flow_start_time: Optional[str] = _field(default=None, metadata={"alias": "flowStartTime"})
    total_flow_num_counted: Optional[bool] = _field(
        default=None, metadata={"alias": "totalFlowNumCounted"}
    )
    total_flow_num_last15_mins_counted: Optional[bool] = _field(
        default=None, metadata={"alias": "totalFlowNumLast15MinsCounted"}
    )


@dataclass
class NwpitraceFlowRespPayloadDataUpActualPath:
    interface: Optional[str] = _field(default=None, metadata={"alias": "Interface"})
    type: Optional[str] = _field(default=None, metadata={"alias": "Type"})


@dataclass
class NwpitraceFlowRespPayloadDataUpstreamDeviceList:
    device_name: Optional[str] = _field(default=None)
    device_system_ip: Optional[str] = _field(default=None)
    down_actual_path: Optional[NwpitraceFlowRespPayloadDataUpActualPath] = _field(default=None)
    down_fwd_decision: Optional[str] = _field(default=None)
    egress_next_invalid: Optional[bool] = _field(default=None)
    ingress_pre_invalid: Optional[bool] = _field(default=None)
    local_color: Optional[str] = _field(default=None, metadata={"alias": "localColor"})
    remote_color: Optional[str] = _field(default=None, metadata={"alias": "remoteColor"})
    up_actual_path: Optional[NwpitraceFlowRespPayloadDataUpActualPath] = _field(default=None)
    up_fwd_decision: Optional[str] = _field(default=None)


@dataclass
class NwpitraceFlowRespPayloadData:
    app_group: Optional[str] = _field(default=None)
    app_name: Optional[str] = _field(default=None)
    appqoe_diverted: Optional[bool] = _field(default=None)
    art: Optional[str] = _field(default=None)
    asymmetry_detected: Optional[bool] = _field(default=None)
    big_drop: Optional[bool] = _field(default=None)
    big_wan_drop: Optional[bool] = _field(default=None)
    device_trace_id: Optional[int] = _field(default=None)
    domain_name: Optional[str] = _field(default=None)
    domain_src: Optional[str] = _field(default=None)
    downstream_device_list: Optional[List[NwpitraceFlowRespPayloadDataDownstreamDeviceList]] = (
        _field(default=None)
    )
    downstream_dscp: Optional[str] = _field(default=None)
    downstream_hop_list: Optional[List[NwpitraceFlowRespPayloadDataDownstreamHopList]] = _field(
        default=None
    )
    dpi_policy_used: Optional[bool] = _field(default=None)
    dst_ip: Optional[str] = _field(default=None)
    dst_port: Optional[int] = _field(default=None)
    dst_sgt: Optional[str] = _field(default=None)
    fif_dpi_not_classified: Optional[bool] = _field(default=None)
    flow_fin: Optional[bool] = _field(default=None)
    flow_id: Optional[int] = _field(default=None)
    flow_key: Optional[str] = _field(default=None)
    flow_moved: Optional[bool] = _field(default=None)
    flow_readout: Optional[NwpitraceFlowRespPayloadDataFlowReadout] = _field(default=None)
    max_local_drop_rate: Optional[int] = _field(default=None)
    max_wan_drop_rate: Optional[int] = _field(default=None)
    nat_translated: Optional[bool] = _field(default=None)
    path_changed: Optional[bool] = _field(default=None)
    policy_bypassed: Optional[bool] = _field(default=None)
    protocol: Optional[str] = _field(default=None)
    qos_congested: Optional[bool] = _field(default=None)
    received_timestamp: Optional[int] = _field(default=None)
    server_no_response: Optional[bool] = _field(default=None)
    sla_violated: Optional[bool] = _field(default=None)
    sla_violated_bfd: Optional[bool] = _field(default=None)
    src_ip: Optional[str] = _field(default=None)
    src_port: Optional[int] = _field(default=None)
    src_sgt: Optional[str] = _field(default=None)
    start_device: Optional[str] = _field(default=None)
    start_timestamp: Optional[int] = _field(default=None)
    tcp_flow_reset: Optional[bool] = _field(default=None)
    test_id: Optional[int] = _field(default=None)
    timestamp: Optional[int] = _field(default=None)
    upstream_device_list: Optional[List[NwpitraceFlowRespPayloadDataUpstreamDeviceList]] = _field(
        default=None
    )
    upstream_dscp: Optional[str] = _field(default=None)
    upstream_hop_list: Optional[List[NwpitraceFlowRespPayloadDataDownstreamHopList]] = _field(
        default=None
    )
    user_group: Optional[str] = _field(default=None)
    user_name: Optional[str] = _field(default=None)
    utd_diverted: Optional[bool] = _field(default=None)
    vpn_id: Optional[str] = _field(default=None)
    wan_color_asym: Optional[bool] = _field(default=None)


@dataclass
class NwpitraceFlowRespPayloadData1:
    data: Optional[NwpitraceFlowRespPayloadData] = _field(default=None)
    entry_time: Optional[int] = _field(default=None)
    tenant: Optional[str] = _field(default=None)
    trace_id: Optional[int] = _field(default=None, metadata={"alias": "trace-id"})
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})


@dataclass
class NwpitraceFlowRespPayload:
    """
    Nwpi traceFlow response payload schema
    """

    data: Optional[List[NwpitraceFlowRespPayloadData1]] = _field(default=None)
