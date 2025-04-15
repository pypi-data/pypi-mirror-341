# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

LocalStatus = Literal["green", "red"]

PeerType = Literal["nonSDWAN", "vbond", "vedge", "vedge-vbond", "vmanage", "vsmart"]

RemoteStatus = Literal["green", "red"]

State = Literal["down", "up"]

TlocStatus = Literal["green", "red"]


@dataclass
class TlocControl:
    host_name: Optional[str] = _field(default=None, metadata={"alias": "host-name"})
    is_preferred: Optional[bool] = _field(default=None, metadata={"alias": "is-preferred"})
    local_status: Optional[LocalStatus] = _field(default=None, metadata={"alias": "local-status"})
    local_status_info: Optional[str] = _field(default=None, metadata={"alias": "local-status-info"})
    peer_type: Optional[PeerType] = _field(default=None, metadata={"alias": "peer-type"})
    remote_status: Optional[RemoteStatus] = _field(
        default=None, metadata={"alias": "remote-status"}
    )
    remote_status_info: Optional[str] = _field(
        default=None, metadata={"alias": "remote-status-info"}
    )
    state: Optional[State] = _field(default=None)
    system_ip: Optional[str] = _field(default=None, metadata={"alias": "system-ip"})


@dataclass
class ControlConnectionInfo:
    actual_connections: Optional[int] = _field(
        default=None, metadata={"alias": "actual-connections"}
    )
    color: Optional[str] = _field(default=None)
    control: Optional[List[TlocControl]] = _field(default=None)
    expected_connections: Optional[int] = _field(
        default=None, metadata={"alias": "expected-connections"}
    )
    interface: Optional[str] = _field(default=None)
    nat_type: Optional[str] = _field(default=None, metadata={"alias": "nat-type"})
    private_ip: Optional[str] = _field(default=None, metadata={"alias": "private-ip"})
    private_port: Optional[str] = _field(default=None, metadata={"alias": "private-port"})
    public_ip: Optional[str] = _field(default=None, metadata={"alias": "public-ip"})
    public_port: Optional[str] = _field(default=None, metadata={"alias": "public-port"})
    tloc_status: Optional[TlocStatus] = _field(default=None, metadata={"alias": "tloc-status"})
    tloc_type: Optional[str] = _field(default=None, metadata={"alias": "tloc-type"})


@dataclass
class GetControlConnections:
    actual_control_connections_to_vsmart: Optional[int] = _field(
        default=None, metadata={"alias": "actualControlConnectionsToVsmart"}
    )
    data: Optional[List[ControlConnectionInfo]] = _field(default=None)
    expected_control_connections_to_vsmart: Optional[int] = _field(
        default=None, metadata={"alias": "expectedControlConnectionsToVsmart"}
    )
