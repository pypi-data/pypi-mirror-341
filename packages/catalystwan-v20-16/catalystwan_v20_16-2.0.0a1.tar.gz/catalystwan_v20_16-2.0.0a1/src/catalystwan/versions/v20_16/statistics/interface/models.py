# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

SortOrderParam = Literal["ASC", "Asc", "DESC", "Desc", "asc", "desc"]


@dataclass
class RuleTypes:
    field: Optional[str] = _field(default=None)
    operator: Optional[str] = _field(default=None)
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})
    value: Optional[List[str]] = _field(default=None)


@dataclass
class QueryWithRule:
    condition: Optional[str] = _field(default=None)
    rules: Optional[RuleTypes] = _field(default=None)


@dataclass
class InterfaceQuery:
    query: Optional[QueryWithRule] = _field(default=None)


@dataclass
class InterfaceResp:
    """
    interface specific response
    """

    device_model: Optional[str] = _field(default=None)
    dst_ip: Optional[str] = _field(default=None)
    dst_port: Optional[int] = _field(default=None)
    entry_time: Optional[str] = _field(default=None)
    fec_re: Optional[int] = _field(default=None)
    fec_rx: Optional[int] = _field(default=None)
    fec_tx: Optional[int] = _field(default=None)
    host_name: Optional[str] = _field(default=None)
    id: Optional[str] = _field(default=None)
    jitter: Optional[int] = _field(default=None)
    latency: Optional[int] = _field(default=None)
    local_color: Optional[str] = _field(default=None)
    local_system_ip: Optional[str] = _field(default=None)
    loss: Optional[int] = _field(default=None)
    loss_percentage: Optional[int] = _field(default=None)
    name: Optional[str] = _field(default=None)
    proto: Optional[str] = _field(default=None)
    remote_color: Optional[str] = _field(default=None)
    remote_system_ip: Optional[str] = _field(default=None)
    rx_octets: Optional[int] = _field(default=None)
    rx_pkts: Optional[int] = _field(default=None)
    sla_class_list: Optional[str] = _field(default=None)
    sla_class_names: Optional[str] = _field(default=None)
    src_ip: Optional[str] = _field(default=None)
    src_port: Optional[int] = _field(default=None)
    statcycletime: Optional[str] = _field(default=None)
    state: Optional[str] = _field(default=None)
    tenant: Optional[str] = _field(default=None)
    total: Optional[int] = _field(default=None)
    tunnel_color: Optional[str] = _field(default=None)
    tx_octets: Optional[int] = _field(default=None)
    tx_pkts: Optional[int] = _field(default=None)
    vdevice_name: Optional[str] = _field(default=None)
    vip_idx: Optional[int] = _field(default=None)
    vmanage_system_ip: Optional[str] = _field(default=None)
    vqoe_score: Optional[int] = _field(default=None)


@dataclass
class PageInfo:
    # number of alarms to be fetched
    count: Optional[int] = _field(default=None)
    # end time of alarms to be fetched
    end_time: Optional[int] = _field(default=None, metadata={"alias": "endTime"})
    # start time of alarms to be fetched
    start_time: Optional[int] = _field(default=None, metadata={"alias": "startTime"})


@dataclass
class InterfaceRespWithPageInfo:
    """
    interface response with page info
    """

    data: Optional[List[InterfaceResp]] = _field(default=None)
    page_info: Optional[PageInfo] = _field(default=None, metadata={"alias": "pageInfo"})
