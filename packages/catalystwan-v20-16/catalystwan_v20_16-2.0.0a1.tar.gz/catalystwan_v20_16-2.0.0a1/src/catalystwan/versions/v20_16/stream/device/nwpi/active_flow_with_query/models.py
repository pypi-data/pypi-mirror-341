# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Optional


@dataclass
class FlowInfoResponseDataDownstreamDeviceList:
    device_name: Optional[str] = _field(default=None)
    device_system_ip: Optional[str] = _field(default=None)
    local_color: Optional[str] = _field(default=None, metadata={"alias": "localColor"})
    remote_color: Optional[str] = _field(default=None, metadata={"alias": "remoteColor"})


@dataclass
class FlowInfoResponseDataDownstreamHopList:
    art: Optional[str] = _field(default=None)
    asymmetry_detected: Optional[bool] = _field(default=None)
    dpi_policy_used: Optional[bool] = _field(default=None)
    fif_dpi_not_classified: Optional[bool] = _field(default=None)


@dataclass
class FlowInfoResponseDataUpstreamDeviceList:
    device_name: Optional[str] = _field(default=None)
    device_system_ip: Optional[str] = _field(default=None)
    ingress_pre_invalid: Optional[bool] = _field(default=None)


@dataclass
class FlowInfoResponseDataUpstreamHopList:
    art: Optional[str] = _field(default=None)
    asymmetry_detected: Optional[bool] = _field(default=None)
    dpi_policy_used: Optional[bool] = _field(default=None)


@dataclass
class FlowInfoResponseData:
    app_group: Optional[str] = _field(default=None)
    app_name: Optional[str] = _field(default=None)
    appqoe_diverted: Optional[bool] = _field(default=None)
    art: Optional[str] = _field(default=None)
    asymmetry_detected: Optional[bool] = _field(default=None)
    big_drop: Optional[bool] = _field(default=None)
    big_wan_drop: Optional[bool] = _field(default=None)
    device_trace_id: Optional[int] = _field(default=None)
    domain: Optional[List[str]] = _field(default=None)
    domain_name: Optional[str] = _field(default=None)
    domain_src: Optional[str] = _field(default=None)
    downstream_device_list: Optional[List[FlowInfoResponseDataDownstreamDeviceList]] = _field(
        default=None
    )
    downstream_dscp: Optional[str] = _field(default=None)
    downstream_hop_list: Optional[FlowInfoResponseDataDownstreamHopList] = _field(default=None)
    dpi_policy_used: Optional[bool] = _field(default=None)
    dst_ip: Optional[str] = _field(default=None)
    dst_port: Optional[int] = _field(default=None)
    dst_sgt: Optional[str] = _field(default=None)
    fif_dpi_not_classified: Optional[bool] = _field(default=None)
    flow_fin: Optional[bool] = _field(default=None)
    flow_id: Optional[int] = _field(default=None)
    flow_key: Optional[str] = _field(default=None)
    flow_moved: Optional[bool] = _field(default=None)
    flow_readout: Optional[Any] = _field(default=None)
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
    timestamp: Optional[int] = _field(default=None)
    upstream_device_list: Optional[List[FlowInfoResponseDataUpstreamDeviceList]] = _field(
        default=None
    )
    upstream_dscp: Optional[str] = _field(default=None)
    upstream_hop_list: Optional[List[FlowInfoResponseDataUpstreamHopList]] = _field(default=None)
    utd_diverted: Optional[bool] = _field(default=None)
    vpn_id: Optional[str] = _field(default=None)
    wan_color_asym: Optional[bool] = _field(default=None)


@dataclass
class ActiveFlowResponsePayload:
    """
    Active flows data response payload
    """

    data: Optional[List[FlowInfoResponseData]] = _field(default=None)
