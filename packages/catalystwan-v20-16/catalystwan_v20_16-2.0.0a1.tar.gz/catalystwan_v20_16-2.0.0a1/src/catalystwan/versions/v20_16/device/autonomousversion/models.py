# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field


@dataclass
class SoftwareVersion:
    active_version: str = _field(metadata={"alias": "activeVersion"})
    lastupdated: int
    vdevice_data_key: str = _field(metadata={"alias": "vdevice-dataKey"})
    vdevice_host_name: str = _field(metadata={"alias": "vdevice-host-name"})
    vdevice_name: str = _field(metadata={"alias": "vdevice-name"})
