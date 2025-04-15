# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class DeviceListEntry:
    device_model: Optional[str] = _field(default=None)
    local_system_ip: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    site_id: Optional[str] = _field(default=None)
    site_name: Optional[str] = _field(default=None)
    system_ip: Optional[str] = _field(default=None)
    uuid: Optional[str] = _field(default=None)


@dataclass
class SupportedDeviceListEntry:
    device_model: Optional[str] = _field(default=None)
    has_estimated: Optional[bool] = _field(default=None, metadata={"alias": "hasEstimated"})
    local_system_ip: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    site_id: Optional[str] = _field(default=None)
    site_name: Optional[str] = _field(default=None)
    system_ip: Optional[str] = _field(default=None)
    uuid: Optional[str] = _field(default=None)


@dataclass
class SupportedDeviceList:
    devices: Optional[List[DeviceListEntry]] = _field(default=None)
    supported_devices: Optional[List[SupportedDeviceListEntry]] = _field(
        default=None, metadata={"alias": "supported-devices"}
    )
