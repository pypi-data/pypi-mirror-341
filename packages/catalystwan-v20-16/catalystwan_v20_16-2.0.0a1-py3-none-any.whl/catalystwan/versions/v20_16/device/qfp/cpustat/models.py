# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class QfpCpuState:
    cpp_num: Optional[str] = _field(default=None, metadata={"alias": "cpp-num"})
    dp_stats_load: Optional[str] = _field(default=None, metadata={"alias": "dp-stats-load"})
    lastupdated: Optional[int] = _field(default=None)
    period: Optional[str] = _field(default=None)
    total_input_bytes: Optional[str] = _field(default=None, metadata={"alias": "total-input-bytes"})
    total_input_pkts: Optional[str] = _field(default=None, metadata={"alias": "total-input-pkts"})
    total_output_bytes: Optional[str] = _field(
        default=None, metadata={"alias": "total-output-bytes"}
    )
    total_output_pkts: Optional[str] = _field(default=None, metadata={"alias": "total-output-pkts"})
    vdevice_data_key: Optional[str] = _field(default=None, metadata={"alias": "vdevice-dataKey"})
    vdevice_host_name: Optional[str] = _field(default=None, metadata={"alias": "vdevice-host-name"})
    vdevice_name: Optional[str] = _field(default=None, metadata={"alias": "vdevice-name"})
