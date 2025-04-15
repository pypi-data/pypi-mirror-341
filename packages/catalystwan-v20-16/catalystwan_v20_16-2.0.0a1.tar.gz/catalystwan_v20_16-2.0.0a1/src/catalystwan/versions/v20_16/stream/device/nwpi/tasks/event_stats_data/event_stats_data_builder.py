# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EventStatsDataResponsePayload


class EventStatsDataBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/tasks/eventStatsData
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, task_id: int, state: str, task_end_time: int, duration: int, **kw
    ) -> EventStatsDataResponsePayload:
        """
        Get auto on stats data in one task
        GET /dataservice/stream/device/nwpi/tasks/eventStatsData

        :param task_id: Task id
        :param state: State
        :param task_end_time: Task end time
        :param duration: Duration
        :returns: EventStatsDataResponsePayload
        """
        logging.warning("Operation: %s is deprecated", "getEventStatsData")
        params = {
            "taskId": task_id,
            "state": state,
            "taskEndTime": task_end_time,
            "duration": duration,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/tasks/eventStatsData",
            return_type=EventStatsDataResponsePayload,
            params=params,
            **kw,
        )
