# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class DeviceHardwareHealthDetail:
    bfd_sessions: Optional[str] = _field(default=None, metadata={"alias": "bfdSessions"})
    board_serial: Optional[str] = _field(default=None, metadata={"alias": "board-serial"})
    control_connections: Optional[str] = _field(
        default=None, metadata={"alias": "controlConnections"}
    )
    cpu_load_display: Optional[str] = _field(default=None, metadata={"alias": "cpuLoadDisplay"})
    device_model: Optional[str] = _field(default=None, metadata={"alias": "device-model"})
    device_type: Optional[str] = _field(default=None, metadata={"alias": "device-type"})
    hardware_state: Optional[str] = _field(default=None, metadata={"alias": "hardwareState"})
    host_name: Optional[str] = _field(default=None, metadata={"alias": "host-name"})
    lastupdated: Optional[int] = _field(default=None)
    local_system_ip: Optional[str] = _field(default=None, metadata={"alias": "local-system-ip"})
    mem_usage_display: Optional[str] = _field(default=None, metadata={"alias": "memUsageDisplay"})
    number_vsmart_peers: Optional[int] = _field(
        default=None, metadata={"alias": "number-vsmart-peers"}
    )
    omp_peers: Optional[str] = _field(default=None, metadata={"alias": "ompPeers"})
    reachability: Optional[str] = _field(default=None)
    site_id: Optional[str] = _field(default=None, metadata={"alias": "site-id"})
    system_ip: Optional[str] = _field(default=None, metadata={"alias": "system-ip"})
    uptime_date: Optional[int] = _field(default=None, metadata={"alias": "uptime-date"})
    uuid: Optional[str] = _field(default=None)
    version: Optional[str] = _field(default=None)
