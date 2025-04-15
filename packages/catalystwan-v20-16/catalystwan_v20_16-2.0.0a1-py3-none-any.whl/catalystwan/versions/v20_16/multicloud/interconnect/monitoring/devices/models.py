# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class InterconnectDeviceInfoExtended:
    config_status_message: Optional[str] = _field(
        default=None, metadata={"alias": "configStatusMessage"}
    )
    configured_system_ip: Optional[str] = _field(
        default=None, metadata={"alias": "configuredSystemIP"}
    )
    device_model: Optional[str] = _field(default=None, metadata={"alias": "device-model"})
    device_type: Optional[str] = _field(default=None, metadata={"alias": "device-type"})
    edge_gateway_name: Optional[str] = _field(default=None, metadata={"alias": "edgeGatewayName"})
    host_name: Optional[str] = _field(default=None, metadata={"alias": "host-name"})
    last_updated: Optional[int] = _field(default=None, metadata={"alias": "lastUpdated"})
    local_system_ip: Optional[str] = _field(default=None, metadata={"alias": "local-system-ip"})
    reachability: Optional[str] = _field(default=None)
    site_id: Optional[str] = _field(default=None, metadata={"alias": "site-id"})
    status: Optional[str] = _field(default=None)
    system_ip: Optional[str] = _field(default=None, metadata={"alias": "system-ip"})
    uptime_date: Optional[int] = _field(default=None, metadata={"alias": "uptimeDate"})
    uuid: Optional[str] = _field(default=None)
    version: Optional[str] = _field(default=None)
