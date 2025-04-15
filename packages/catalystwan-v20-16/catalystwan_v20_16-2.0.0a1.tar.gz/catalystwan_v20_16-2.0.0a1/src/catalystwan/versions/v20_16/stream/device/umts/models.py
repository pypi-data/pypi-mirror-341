# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class UmtsSession:
    download_status: Optional[str] = _field(default=None)
    payload: Optional[str] = _field(default=None)
    renewal_time: Optional[int] = _field(default=None, metadata={"alias": "renewalTime"})
    request_status: Optional[str] = _field(default=None, metadata={"alias": "requestStatus"})
    session_id: Optional[str] = _field(default=None, metadata={"alias": "sessionId"})
    start_time: Optional[int] = _field(default=None, metadata={"alias": "startTime"})
    status: Optional[str] = _field(default=None)
    status_message: Optional[str] = _field(default=None, metadata={"alias": "statusMessage"})
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})
    user: Optional[str] = _field(default=None)
    user_ip: Optional[str] = _field(default=None, metadata={"alias": "userIp"})
    uuid: Optional[str] = _field(default=None)


@dataclass
class UmtsInput:
    device_uuid: Optional[str] = _field(default=None, metadata={"alias": "deviceUUID"})
    local_color: Optional[str] = _field(default=None, metadata={"alias": "localColor"})
    remote_color: Optional[str] = _field(default=None, metadata={"alias": "remoteColor"})
    remote_system: Optional[str] = _field(default=None, metadata={"alias": "remoteSystem"})
