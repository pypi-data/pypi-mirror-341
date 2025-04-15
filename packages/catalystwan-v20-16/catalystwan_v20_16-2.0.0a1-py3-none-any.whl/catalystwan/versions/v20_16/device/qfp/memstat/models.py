# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class QfpMemoryState:
    dram_free: Optional[int] = _field(default=None, metadata={"alias": "dramFree"})
    dram_in_use: Optional[int] = _field(default=None, metadata={"alias": "dramInUse"})
    dram_lowest_free_water_mark: Optional[int] = _field(
        default=None, metadata={"alias": "dramLowestFreeWaterMark"}
    )
    dram_total: Optional[int] = _field(default=None, metadata={"alias": "dramTotal"})
    iram_free: Optional[int] = _field(default=None, metadata={"alias": "iramFree"})
    iram_in_use: Optional[int] = _field(default=None, metadata={"alias": "iramInUse"})
    iram_lowest_free_water_mark: Optional[int] = _field(
        default=None, metadata={"alias": "iramLowestFreeWaterMark"}
    )
    iram_total: Optional[int] = _field(default=None, metadata={"alias": "iramTotal"})
    lastupdated: Optional[int] = _field(default=None)
    sram_free: Optional[int] = _field(default=None, metadata={"alias": "sramFree"})
    sram_in_use: Optional[int] = _field(default=None, metadata={"alias": "sramInUse"})
    sram_lowest_free_water_mark: Optional[int] = _field(
        default=None, metadata={"alias": "sramLowestFreeWaterMark"}
    )
    sram_total: Optional[int] = _field(default=None, metadata={"alias": "sramTotal"})
    vdevice_data_key: Optional[str] = _field(default=None, metadata={"alias": "vdevice-dataKey"})
    vdevice_host_name: Optional[str] = _field(default=None, metadata={"alias": "vdevice-host-name"})
    vdevice_name: Optional[str] = _field(default=None, metadata={"alias": "vdevice-name"})
