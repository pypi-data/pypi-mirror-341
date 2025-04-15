# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class DpiDataObject:
    application: Optional[str] = _field(default=None)
    create_time: Optional[int] = _field(default=None)
    dest_ip: Optional[str] = _field(default=None)
    dest_port: Optional[int] = _field(default=None)
    device_model: Optional[str] = _field(default=None)
    entry_time: Optional[int] = _field(default=None)
    expire_time: Optional[int] = _field(default=None)
    family: Optional[str] = _field(default=None)
    host_name: Optional[str] = _field(default=None)
    ip_proto: Optional[int] = _field(default=None)
    octets: Optional[int] = _field(default=None)
    packets: Optional[int] = _field(default=None)
    source_ip: Optional[str] = _field(default=None)
    source_port: Optional[int] = _field(default=None)
    vdevice_name: Optional[str] = _field(default=None)
    vip_idx: Optional[int] = _field(default=None)
    vpn_id: Optional[int] = _field(default=None)


@dataclass
class DpiPaginationResponsePageInfo:
    count: Optional[int] = _field(default=None)
    end_time: Optional[str] = _field(default=None, metadata={"alias": "endTime"})
    has_more_data: Optional[str] = _field(default=None, metadata={"alias": "hasMoreData"})
    scroll_id: Optional[str] = _field(default=None, metadata={"alias": "scrollId"})
    start_time: Optional[str] = _field(default=None, metadata={"alias": "startTime"})
    total_count: Optional[int] = _field(default=None, metadata={"alias": "totalCount"})


@dataclass
class DpiPaginationResponse:
    data: Optional[List[DpiDataObject]] = _field(default=None)
    page_info: Optional[DpiPaginationResponsePageInfo] = _field(
        default=None, metadata={"alias": "pageInfo"}
    )
