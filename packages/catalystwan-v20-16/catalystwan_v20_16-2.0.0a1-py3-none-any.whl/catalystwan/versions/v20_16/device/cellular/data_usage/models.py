# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

LastNHoursParam = Literal["1", "12", "24", "3", "6"]


@dataclass
class CellularDeviceDetail:
    active_sim: Optional[str] = _field(default=None, metadata={"alias": "activeSim"})
    carrier: Optional[str] = _field(default=None)
    device_type: Optional[str] = _field(default=None, metadata={"alias": "deviceType"})
    host_name: Optional[str] = _field(default=None, metadata={"alias": "hostName"})
    if_name: Optional[str] = _field(default=None, metadata={"alias": "ifName"})
    link_up_time: Optional[str] = _field(default=None, metadata={"alias": "linkUpTime"})
    local_system_ip: Optional[str] = _field(default=None, metadata={"alias": "localSystemIp"})
    model: Optional[str] = _field(default=None)
    product: Optional[str] = _field(default=None)
    rat: Optional[str] = _field(default=None)
    slot: Optional[str] = _field(default=None)
    system_ip: Optional[str] = _field(default=None, metadata={"alias": "systemIp"})
    total_kbs: Optional[int] = _field(default=None, metadata={"alias": "totalKbs"})
    uuid: Optional[str] = _field(default=None)


@dataclass
class CellularDataUsageDetailsItem:
    carrier_name: Optional[str] = _field(default=None, metadata={"alias": "carrierName"})
    device_list: Optional[List[CellularDeviceDetail]] = _field(
        default=None, metadata={"alias": "deviceList"}
    )
    total_usage: Optional[int] = _field(default=None, metadata={"alias": "totalUsage"})


@dataclass
class CellularDataUsageDetails:
    carrier_name: Optional[str] = _field(default=None, metadata={"alias": "carrierName"})
    device_list: Optional[List[CellularDeviceDetail]] = _field(
        default=None, metadata={"alias": "deviceList"}
    )
    month_usage: Optional[CellularDataUsageDetailsItem] = _field(
        default=None, metadata={"alias": "monthUsage"}
    )
    one_day_usage: Optional[CellularDataUsageDetailsItem] = _field(
        default=None, metadata={"alias": "oneDayUsage"}
    )
    three_month_usage: Optional[CellularDataUsageDetailsItem] = _field(
        default=None, metadata={"alias": "threeMonthUsage"}
    )
    total_usage: Optional[int] = _field(default=None, metadata={"alias": "totalUsage"})
    week_usage: Optional[CellularDataUsageDetailsItem] = _field(
        default=None, metadata={"alias": "weekUsage"}
    )


@dataclass
class CellularDataUsageBasicItem:
    carrier_name: Optional[str] = _field(default=None, metadata={"alias": "carrierName"})
    total_usage: Optional[int] = _field(default=None, metadata={"alias": "totalUsage"})


@dataclass
class CellularDataUsage:
    carrier_name: Optional[CellularDataUsageDetails] = _field(
        default=None, metadata={"alias": "CARRIER_NAME"}
    )
    details: Optional[List[CellularDataUsageBasicItem]] = _field(default=None)
