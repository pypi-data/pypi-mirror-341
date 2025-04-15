# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class PowerConsumptionDeviceEntry:
    change: Optional[int] = _field(default=None)
    cost: Optional[int] = _field(default=None)
    device_model: Optional[str] = _field(default=None)
    device_type: Optional[str] = _field(default=None)
    emission: Optional[int] = _field(default=None)
    local_system_ip: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    power_usage: Optional[int] = _field(default=None)
    site_id: Optional[str] = _field(default=None)
    site_name: Optional[str] = _field(default=None)
    system_ip: Optional[str] = _field(default=None)
    uuid: Optional[str] = _field(default=None)


@dataclass
class PowerConsumptionSiteEntry:
    change: Optional[int] = _field(default=None)
    cost: Optional[int] = _field(default=None)
    devices: Optional[List[PowerConsumptionDeviceEntry]] = _field(default=None)
    emission: Optional[int] = _field(default=None)
    power_usage: Optional[int] = _field(default=None)
    site_id: Optional[str] = _field(default=None)
    site_name: Optional[str] = _field(default=None)


@dataclass
class PowerConsumptionDeviceResp:
    data: Optional[List[PowerConsumptionSiteEntry]] = _field(default=None)
