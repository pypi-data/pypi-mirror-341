# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class TraceInfoResponsePayloadSummary:
    agg_client_prefix: Optional[str] = _field(default=None, metadata={"alias": "agg-client-prefix"})
    agg_src_sgt: Optional[str] = _field(default=None, metadata={"alias": "agg-src-sgt"})
    agg_svr_prefix: Optional[str] = _field(default=None, metadata={"alias": "agg-svr-prefix"})
    app: Optional[str] = _field(default=None)
    app_grp: Optional[str] = _field(default=None, metadata={"alias": "app-grp"})
    app_vis: Optional[str] = _field(default=None, metadata={"alias": "app-vis"})
    art_vis: Optional[str] = _field(default=None, metadata={"alias": "art-vis"})
    common_app: Optional[str] = _field(default=None)
    device_ip: Optional[str] = _field(default=None, metadata={"alias": "device-ip"})
    dia_vis: Optional[str] = _field(default=None, metadata={"alias": "dia-vis"})
    domain_mon: Optional[str] = _field(default=None, metadata={"alias": "domain-mon"})
    dscp: Optional[str] = _field(default=None)
    dst_ip: Optional[str] = _field(default=None, metadata={"alias": "dst-ip"})
    dst_pfx: Optional[str] = _field(default=None, metadata={"alias": "dst-pfx"})
    dst_pfx_len: Optional[str] = _field(default=None, metadata={"alias": "dst-pfx-len"})
    dst_port: Optional[str] = _field(default=None, metadata={"alias": "dst-port"})
    duration: Optional[str] = _field(default=None)
    hub_wan_vis: Optional[str] = _field(default=None, metadata={"alias": "hub-wan-vis"})
    local_drop_rate_threshold: Optional[int] = _field(
        default=None, metadata={"alias": "local-drop-rate-threshold"}
    )
    message: Optional[str] = _field(default=None)
    protocol: Optional[str] = _field(default=None)
    qos_mon: Optional[str] = _field(default=None, metadata={"alias": "qos-mon"})
    sampling: Optional[str] = _field(default=None)
    source_site: Optional[str] = _field(default=None, metadata={"alias": "source-site"})
    source_site_vmanage_version: Optional[str] = _field(
        default=None, metadata={"alias": "source-site-vmanage-version"}
    )
    spl_intvl: Optional[str] = _field(default=None, metadata={"alias": "spl-intvl"})
    src_if: Optional[str] = _field(default=None, metadata={"alias": "src-if"})
    src_ip: Optional[str] = _field(default=None, metadata={"alias": "src-ip"})
    src_pfx: Optional[str] = _field(default=None, metadata={"alias": "src-pfx"})
    src_pfx_len: Optional[str] = _field(default=None, metadata={"alias": "src-pfx-len"})
    src_port: Optional[str] = _field(default=None, metadata={"alias": "src-port"})
    state: Optional[str] = _field(default=None)
    stop_time: Optional[int] = _field(default=None, metadata={"alias": "stop-time"})
    task_id: Optional[int] = _field(default=None, metadata={"alias": "taskId"})
    trace_name: Optional[str] = _field(default=None, metadata={"alias": "trace-name"})
    trace_trigger_event: Optional[str] = _field(
        default=None, metadata={"alias": "trace-trigger-event"}
    )
    vpn_id: Optional[str] = _field(default=None, metadata={"alias": "vpn-id"})
    vpn_list: Optional[str] = _field(default=None, metadata={"alias": "vpn-list"})
    wan_drop_rate_threshold: Optional[int] = _field(
        default=None, metadata={"alias": "wan-drop-rate-threshold"}
    )
    warning: Optional[str] = _field(default=None)


@dataclass
class TraceInfoResponsePayload:
    """
    Trace base info Data Response schema
    """

    entry_time: Optional[int] = _field(default=None)
    summary: Optional[TraceInfoResponsePayloadSummary] = _field(default=None)
    trace_id: Optional[int] = _field(default=None, metadata={"alias": "trace-id"})
