# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

Reachability = Literal["reachable", "unreachable"]

Status = Literal["error", "new", "normal", "warning"]

Validity = Literal["invalid", "prestaging", "staging", "valid"]


@dataclass
class Loopback:
    interface_ip: Optional[str] = _field(default=None, metadata={"alias": "interfaceIP"})
    interface_name: Optional[str] = _field(default=None, metadata={"alias": "interfaceName"})


@dataclass
class Device:
    chassis_serial_number: Optional[str] = _field(
        default=None, metadata={"alias": "chassis-serial-number"}
    )
    configured_aaa_user: Optional[List[str]] = _field(
        default=None, metadata={"alias": "configuredAaaUser"}
    )
    device_id: Optional[str] = _field(default=None, metadata={"alias": "deviceId"})
    device_model: Optional[str] = _field(default=None, metadata={"alias": "device-model"})
    device_os: Optional[str] = _field(default=None, metadata={"alias": "device-os"})
    device_type: Optional[str] = _field(default=None, metadata={"alias": "device-type"})
    devices_attached: Optional[int] = _field(default=None, metadata={"alias": "devicesAttached"})
    discovered_device_interfaces: Optional[List[str]] = _field(
        default=None, metadata={"alias": "discoveredDeviceInterfaces"}
    )
    host_name: Optional[str] = _field(default=None, metadata={"alias": "host-name"})
    loopback: Optional[List[Loopback]] = _field(default=None)
    personality: Optional[str] = _field(default=None)
    platform: Optional[str] = _field(default=None)
    reachability: Optional[Reachability] = _field(default=None)
    registration_date: Optional[int] = _field(default=None, metadata={"alias": "registrationDate"})
    serial_number: Optional[str] = _field(default=None, metadata={"alias": "serialNumber"})
    site_id: Optional[str] = _field(default=None, metadata={"alias": "site-id"})
    state: Optional[str] = _field(default=None)
    status: Optional[Status] = _field(default=None)
    system_ip: Optional[str] = _field(default=None, metadata={"alias": "system-ip"})
    template_status: Optional[str] = _field(default=None, metadata={"alias": "templateStatus"})
    uuid: Optional[str] = _field(default=None)
    validity: Optional[Validity] = _field(default=None)
    version: Optional[str] = _field(default=None)
    wan_interfaces: Optional[List[str]] = _field(default=None, metadata={"alias": "wanInterfaces"})
