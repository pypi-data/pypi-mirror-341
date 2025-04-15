# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional

Severity = Literal["Critical", "Major", "Medium", "Minor"]


@dataclass
class AlarmDevices:
    system_ip: Optional[str] = _field(default=None, metadata={"alias": "system-ip"})


@dataclass
class GeneralSchema:
    empty: Optional[bool] = _field(default=None)


@dataclass
class Alarm:
    """
    Represents any kind of alarm
    """

    acknowledged: Optional[bool] = _field(default=None)
    active: Optional[bool] = _field(default=None)
    cleared_by: Optional[str] = _field(default=None)
    cleared_events: Optional[List[str]] = _field(default=None)
    cleared_time: Optional[int] = _field(default=None)
    component: Optional[str] = _field(default=None)
    consumed_events: Optional[List[Any]] = _field(default=None)
    devices: Optional[List[AlarmDevices]] = _field(default=None)
    entry_time: Optional[int] = _field(default=None)
    eventname: Optional[str] = _field(default=None)
    id: Optional[str] = _field(default=None)
    message: Optional[str] = _field(default=None)
    possible_causes: Optional[List[str]] = _field(default=None)
    receive_time: Optional[int] = _field(default=None)
    rule_name_display: Optional[str] = _field(default=None)
    rulename: Optional[str] = _field(default=None)
    severity: Optional[Severity] = _field(default=None)
    severity_number: Optional[int] = _field(default=None)
    site_id: Optional[int] = _field(default=None)
    statcycletime: Optional[int] = _field(default=None)
    suppressed: Optional[bool] = _field(default=None)
    suppressed_by: Optional[Any] = _field(default=None)
    system_ip: Optional[str] = _field(default=None)
    tenant: Optional[str] = _field(default=None)
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})
    uuid: Optional[str] = _field(default=None)
    values: Optional[List[GeneralSchema]] = _field(default=None)
    values_short_display: Optional[List[GeneralSchema]] = _field(default=None)


@dataclass
class PageInfo:
    # number of alarms to be fetched
    count: Optional[int] = _field(default=None)
    # end time of alarms to be fetched
    end_time: Optional[int] = _field(default=None, metadata={"alias": "endTime"})
    # start time of alarms to be fetched
    start_time: Optional[int] = _field(default=None, metadata={"alias": "startTime"})


@dataclass
class AlarmResponse:
    """
    AlarmResponse is used for GET/POST /alarms call.
    """

    data: Optional[List[Alarm]] = _field(default=None)
    page_info: Optional[PageInfo] = _field(default=None, metadata={"alias": "pageInfo"})
