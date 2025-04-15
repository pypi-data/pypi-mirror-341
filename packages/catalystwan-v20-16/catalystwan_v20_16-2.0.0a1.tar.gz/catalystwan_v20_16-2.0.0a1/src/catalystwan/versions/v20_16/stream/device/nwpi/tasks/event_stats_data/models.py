# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class EventStatsDataResponsePayloadDataEventStatsObjectEventStatsList:
    event_counter: Optional[int] = _field(default=None)
    event_failed_to_trace_counter: Optional[int] = _field(default=None)
    event_name: Optional[str] = _field(default=None)
    event_to_trace_counter: Optional[int] = _field(default=None)


@dataclass
class EventStatsDataResponsePayloadDataEventStatsObject:
    event_stats_list: Optional[
        List[EventStatsDataResponsePayloadDataEventStatsObjectEventStatsList]
    ] = _field(default=None)
    total_event_counter: Optional[int] = _field(default=None)


@dataclass
class EventStatsDataResponsePayloadData:
    device_site_id: Optional[str] = _field(default=None)
    event_stats_object: Optional[EventStatsDataResponsePayloadDataEventStatsObject] = _field(
        default=None
    )


@dataclass
class EventStatsDataResponsePayloadData1:
    auto_on_task_id: Optional[int] = _field(default=None, metadata={"alias": "auto-on-task-id"})
    data: Optional[EventStatsDataResponsePayloadData] = _field(default=None)
    tenant: Optional[str] = _field(default=None)
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})


@dataclass
class EventStatsDataResponsePayload:
    """
    Event Stats Data schema for GET response
    """

    data: Optional[List[EventStatsDataResponsePayloadData1]] = _field(default=None)
