# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class SdaDeviceConfigRes:
    id: Optional[str] = _field(default=None)


@dataclass
class DeviceConfig:
    device_config: Optional[str] = _field(default=None, metadata={"alias": "deviceConfig"})
    device_id: Optional[str] = _field(default=None, metadata={"alias": "deviceId"})


@dataclass
class VpnListResHeader:
    generated_on: Optional[int] = _field(default=None, metadata={"alias": "generatedOn"})


@dataclass
class SdaConfigRequest:
    data: Optional[List[DeviceConfig]] = _field(default=None)
    header: Optional[VpnListResHeader] = _field(default=None)
