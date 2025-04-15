# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class RealTimeData:
    component_cname: Optional[str] = _field(default=None, metadata={"alias": "component-cname"})
    lastupdated: Optional[int] = _field(default=None)
    platform_property_configurable: Optional[str] = _field(
        default=None, metadata={"alias": "platform-property-configurable"}
    )
    platform_property_name: Optional[str] = _field(
        default=None, metadata={"alias": "platform-property-name"}
    )
    value_string: Optional[str] = _field(default=None, metadata={"alias": "value-string"})
    vdevice_data_key: Optional[str] = _field(default=None, metadata={"alias": "vdevice-dataKey"})
    vdevice_host_name: Optional[str] = _field(default=None, metadata={"alias": "vdevice-host-name"})
    vdevice_name: Optional[str] = _field(default=None, metadata={"alias": "vdevice-name"})


@dataclass
class PowerConsumptionRealTime:
    data: Optional[List[RealTimeData]] = _field(default=None)


@dataclass
class DeviceIp:
    """
    This is the valid DeviceIP
    """

    device_ip: Optional[str] = _field(default=None, metadata={"alias": "deviceIp"})
