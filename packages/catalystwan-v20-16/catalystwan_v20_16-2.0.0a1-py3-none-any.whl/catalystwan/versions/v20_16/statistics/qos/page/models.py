# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class QoSResp:
    """
    QOS specific response
    """

    device_model: Optional[str] = _field(default=None)
    drop_in_bytes: Optional[int] = _field(default=None)
    drop_in_kbps: Optional[int] = _field(default=None)
    drop_in_pkts: Optional[int] = _field(default=None)
    drop_in_pps: Optional[int] = _field(default=None)
    entry_time: Optional[str] = _field(default=None)
    host_name: Optional[str] = _field(default=None)
    id: Optional[str] = _field(default=None)
    interface: Optional[str] = _field(default=None)
    queue_name: Optional[str] = _field(default=None)
    queued_bytes: Optional[int] = _field(default=None)
    queued_bytes_in_kbps: Optional[int] = _field(default=None)
    queued_pkts: Optional[int] = _field(default=None)
    red_drop_bytes: Optional[int] = _field(default=None)
    red_drop_pkts: Optional[int] = _field(default=None)
    statcycletime: Optional[str] = _field(default=None)
    tail_drop_bytes: Optional[int] = _field(default=None)
    tail_drop_pkts: Optional[int] = _field(default=None)
    tenant: Optional[str] = _field(default=None)
    time_interval: Optional[int] = _field(default=None)
    tx_bytes: Optional[int] = _field(default=None)
    tx_bytes_in_kbps: Optional[int] = _field(default=None)
    tx_bytes_in_pps: Optional[int] = _field(default=None)
    tx_pkts: Optional[int] = _field(default=None)
    vdevice_name: Optional[str] = _field(default=None)
    vip_idx: Optional[str] = _field(default=None)
    vip_time: Optional[str] = _field(default=None)
    vmanage_system_ip: Optional[str] = _field(default=None)


@dataclass
class PageInfo:
    # number of alarms to be fetched
    count: Optional[int] = _field(default=None)
    # end time of alarms to be fetched
    end_time: Optional[int] = _field(default=None, metadata={"alias": "endTime"})
    # start time of alarms to be fetched
    start_time: Optional[int] = _field(default=None, metadata={"alias": "startTime"})


@dataclass
class QoSRespWithPageInfo:
    """
    QoS response with page info
    """

    data: Optional[List[QoSResp]] = _field(default=None)
    page_info: Optional[PageInfo] = _field(default=None, metadata={"alias": "pageInfo"})
