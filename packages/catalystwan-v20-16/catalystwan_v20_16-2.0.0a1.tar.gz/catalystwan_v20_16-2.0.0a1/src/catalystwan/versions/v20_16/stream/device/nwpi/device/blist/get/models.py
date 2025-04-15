# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class DeviceBlistResponsePayloadInner:
    """
    Device blist response payload
    """

    crash_time: Optional[int] = _field(default=None, metadata={"alias": "crashTime"})
    crash_version: Optional[str] = _field(default=None, metadata={"alias": "crashVersion"})
    crashed_reason: Optional[str] = _field(default=None, metadata={"alias": "crashedReason"})
    device_blist_state: Optional[str] = _field(default=None, metadata={"alias": "deviceBlistState"})
    device_model: Optional[str] = _field(default=None, metadata={"alias": "deviceModel"})
    device_name: Optional[str] = _field(default=None, metadata={"alias": "deviceName"})
    nwpi_state: Optional[str] = _field(default=None, metadata={"alias": "nwpiState"})
    site_id: Optional[int] = _field(default=None, metadata={"alias": "siteId"})
    system_ip: Optional[str] = _field(default=None, metadata={"alias": "systemIp"})
    type_: Optional[int] = _field(default=None, metadata={"alias": "type"})
