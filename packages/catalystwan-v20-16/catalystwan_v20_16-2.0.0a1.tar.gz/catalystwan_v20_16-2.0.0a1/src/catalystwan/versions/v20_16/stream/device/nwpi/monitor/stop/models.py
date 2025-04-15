# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class NwpiMonitorRespPayload:
    """
    Nwpi monitor response payload schema
    """

    message: Optional[str] = _field(default=None)
    monitor_state: Optional[str] = _field(default=None, metadata={"alias": "monitor-state"})


@dataclass
class NwpiMonitorReqPayloadMapping:
    domain_id: Optional[int] = _field(default=None, metadata={"alias": "domainId"})
    uuid: Optional[str] = _field(default=None)


@dataclass
class NwpiMonitorReqPayloadDeviceToDomainId:
    domain: Optional[str] = _field(default=None)
    mapping: Optional[List[NwpiMonitorReqPayloadMapping]] = _field(default=None)


@dataclass
class NwpiMonitorReqPayloadDomainList:
    domain: Optional[str] = _field(default=None)
    resolved_ip: Optional[List[str]] = _field(default=None, metadata={"alias": "resolvedIp"})


@dataclass
class NwpiMonitorReqPayload:
    """
    Nwpi monitor payload schema
    """

    client_ip: Optional[str] = _field(default=None, metadata={"alias": "clientIp"})
    device_to_domain_id: Optional[List[NwpiMonitorReqPayloadDeviceToDomainId]] = _field(
        default=None, metadata={"alias": "deviceToDomainId"}
    )
    domain_app_grp: Optional[str] = _field(default=None, metadata={"alias": "domainAppGrp"})
    domain_app_vis: Optional[str] = _field(default=None, metadata={"alias": "domainAppVis"})
    domain_list: Optional[List[NwpiMonitorReqPayloadDomainList]] = _field(
        default=None, metadata={"alias": "domainList"}
    )
    trace_id: Optional[str] = _field(default=None, metadata={"alias": "traceId"})
