# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class GetAllUnclaimedDevices:
    _rid: Optional[int] = _field(default=None, metadata={"alias": "@rid"})
    chassis_number: Optional[str] = _field(default=None, metadata={"alias": "chassis-number"})
    create_time_stamp: Optional[int] = _field(default=None, metadata={"alias": "createTimeStamp"})
    lastupdated: Optional[int] = _field(default=None)
    org: Optional[str] = _field(default=None)
    serial_number: Optional[str] = _field(default=None, metadata={"alias": "serial-number"})
    status: Optional[str] = _field(default=None)
    subject_serial_number: Optional[str] = _field(
        default=None, metadata={"alias": "subject-serial-number"}
    )
    vdevice_data_key: Optional[str] = _field(default=None, metadata={"alias": "vdevice-dataKey"})
    vdevice_host_name: Optional[str] = _field(default=None, metadata={"alias": "vdevice-host-name"})
    vdevice_name: Optional[str] = _field(default=None, metadata={"alias": "vdevice-name"})
    vmanage_system_ip: Optional[str] = _field(default=None, metadata={"alias": "vmanage-system-ip"})
