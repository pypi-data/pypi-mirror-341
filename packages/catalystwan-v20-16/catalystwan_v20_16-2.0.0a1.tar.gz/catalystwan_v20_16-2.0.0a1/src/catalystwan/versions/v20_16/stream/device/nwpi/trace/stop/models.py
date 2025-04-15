# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class NwpiTraceStopRespPayloadTraces:
    action: Optional[str] = _field(default=None)
    device_ip: Optional[str] = _field(default=None, metadata={"alias": "device-ip"})
    entry_time: Optional[int] = _field(default=None)
    local_system_ip: Optional[str] = _field(default=None, metadata={"alias": "local-system-ip"})
    message: Optional[str] = _field(default=None)
    trace_id: Optional[int] = _field(default=None, metadata={"alias": "trace-id"})
    uuid: Optional[str] = _field(default=None)


@dataclass
class NwpiTraceStopRespPayload:
    """
    Nwpi trace stoppayload schema
    """

    action: Optional[str] = _field(default=None)
    domain_mon: Optional[bool] = _field(default=None, metadata={"alias": "domain-mon"})
    entry_time: Optional[int] = _field(default=None)
    message: Optional[str] = _field(default=None)
    qos_mon: Optional[bool] = _field(default=None, metadata={"alias": "qos-mon"})
    state: Optional[str] = _field(default=None)
    trace_id: Optional[str] = _field(default=None, metadata={"alias": "trace-id"})
    trace_name: Optional[str] = _field(default=None, metadata={"alias": "trace-name"})
    traces: Optional[List[NwpiTraceStopRespPayloadTraces]] = _field(default=None)
