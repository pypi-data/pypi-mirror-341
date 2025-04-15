# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

OrderByParam = Literal["asc", "desc"]


@dataclass
class DeviceCheckList:
    message: Optional[str] = _field(default=None)
    status: Optional[str] = _field(default=None)
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})


@dataclass
class DeviceApiDetails:
    chassis_number: Optional[str] = _field(default=None, metadata={"alias": "chassis-Number"})
    current_version: Optional[str] = _field(default=None, metadata={"alias": "current-version"})
    device_type: Optional[str] = _field(default=None, metadata={"alias": "device-type"})
    host_name: Optional[str] = _field(default=None, metadata={"alias": "host-name"})
    local_system_ip: Optional[str] = _field(default=None, metadata={"alias": "local-system-ip"})
    personality: Optional[str] = _field(default=None)
    reachability: Optional[str] = _field(default=None)
    site_id: Optional[str] = _field(default=None, metadata={"alias": "site-id"})
    site_name: Optional[str] = _field(default=None, metadata={"alias": "site-name"})
    system_ip: Optional[str] = _field(default=None, metadata={"alias": "system-ip"})
    uuid: Optional[str] = _field(default=None)


@dataclass
class DeviceComplianceApiData:
    check_list: Optional[List[DeviceCheckList]] = _field(
        default=None, metadata={"alias": "checkList"}
    )
    device_details: Optional[DeviceApiDetails] = _field(
        default=None, metadata={"alias": "deviceDetails"}
    )
    status: Optional[str] = _field(default=None)


@dataclass
class DeviceComplianceApiResponse:
    count: Optional[int] = _field(default=None)
    devices: Optional[List[DeviceComplianceApiData]] = _field(default=None)
