# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class AdminTechCreateReq:
    custom_commands: Optional[List[str]] = _field(
        default=None, metadata={"alias": "custom-commands"}
    )
    device_ip: Optional[str] = _field(default=None, metadata={"alias": "deviceIP"})
    device_type: Optional[str] = _field(default=None, metadata={"alias": "device-type"})
    exclude_cores: Optional[bool] = _field(default=None, metadata={"alias": "exclude-cores"})
    exclude_logs: Optional[bool] = _field(default=None, metadata={"alias": "exclude-logs"})
    exclude_tech: Optional[bool] = _field(default=None, metadata={"alias": "exclude-tech"})
    tech_filter: Optional[List[str]] = _field(default=None, metadata={"alias": "tech-filter"})
