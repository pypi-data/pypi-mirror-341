# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class GetTenantManagementSystemIPsInner:
    chasis_number: Optional[str] = _field(default=None, metadata={"alias": "chasisNumber"})
    device_type: Optional[str] = _field(default=None, metadata={"alias": "deviceType"})
    management_system_ip: Optional[str] = _field(
        default=None, metadata={"alias": "managementSystemIP"}
    )
    serial_number: Optional[str] = _field(default=None, metadata={"alias": "serialNumber"})
