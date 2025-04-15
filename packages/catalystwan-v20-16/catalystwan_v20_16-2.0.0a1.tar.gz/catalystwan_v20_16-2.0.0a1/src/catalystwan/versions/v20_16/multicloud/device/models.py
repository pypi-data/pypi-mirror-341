# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class WanEdgeDevicesResponse:
    configured_host_name: Optional[str] = _field(
        default=None, metadata={"alias": "configuredHostName"}
    )
    configured_system_ip: Optional[str] = _field(
        default=None, metadata={"alias": "configuredSystemIp"}
    )
    device_model: Optional[str] = _field(default=None, metadata={"alias": "deviceModel"})
    is_payg_uuid: Optional[bool] = _field(default=None, metadata={"alias": "isPaygUuid"})
    uuid: Optional[str] = _field(default=None)
