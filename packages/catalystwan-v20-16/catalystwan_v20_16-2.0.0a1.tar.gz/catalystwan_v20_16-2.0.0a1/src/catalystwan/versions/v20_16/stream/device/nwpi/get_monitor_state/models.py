# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class NwpiDomainMonitorStateRespPayloadDevicelist:
    app_vis: Optional[str] = _field(default=None, metadata={"alias": "app-vis"})
    art_vis: Optional[str] = _field(default=None, metadata={"alias": "art-vis"})
    connected_v_manages: Optional[str] = _field(
        default=None, metadata={"alias": "connectedVManages"}
    )
    device_ip: Optional[str] = _field(default=None, metadata={"alias": "device-ip"})
    device_type: Optional[str] = _field(default=None, metadata={"alias": "device-type"})
    dia_vis: Optional[str] = _field(default=None, metadata={"alias": "dia-vis"})
    domain_mon: Optional[str] = _field(default=None, metadata={"alias": "domain-mon"})
    domain_monitor_can_be_started: Optional[str] = _field(default=None)
    dscp_is_valid: Optional[str] = _field(default=None, metadata={"alias": "dscp-is-valid"})
    duration: Optional[str] = _field(default=None)
    entry_time: Optional[int] = _field(default=None)
    expire_time: Optional[int] = _field(default=None, metadata={"alias": "expire-time"})
    local_system_ip: Optional[str] = _field(default=None, metadata={"alias": "local-system-ip"})
    message: Optional[str] = _field(default=None)
    parent_trace_id: Optional[int] = _field(default=None, metadata={"alias": "parent-trace-id"})
    qos_mon: Optional[str] = _field(default=None, metadata={"alias": "qos-mon"})
    site_id: Optional[str] = _field(default=None, metadata={"alias": "site-id"})
    source_site: Optional[str] = _field(default=None, metadata={"alias": "source-site"})
    state: Optional[str] = _field(default=None)
    trace_id: Optional[int] = _field(default=None, metadata={"alias": "trace-id"})
    trace_name: Optional[str] = _field(default=None, metadata={"alias": "trace-name"})
    uuid: Optional[str] = _field(default=None)
    version: Optional[str] = _field(default=None)
    vpn_id: Optional[str] = _field(default=None, metadata={"alias": "vpn-id"})


@dataclass
class NwpiDomainMonitorStateRespPayload:
    """
    Nwpi get MonitorState response payload
    """

    device_list: Optional[List[NwpiDomainMonitorStateRespPayloadDevicelist]] = _field(
        default=None, metadata={"alias": "device-list"}
    )
    entry_time: Optional[str] = _field(default=None)
    message: Optional[str] = _field(default=None)
    monitor_state: Optional[str] = _field(default=None, metadata={"alias": "monitor-state"})
    trace_id: Optional[int] = _field(default=None, metadata={"alias": "trace-id"})
