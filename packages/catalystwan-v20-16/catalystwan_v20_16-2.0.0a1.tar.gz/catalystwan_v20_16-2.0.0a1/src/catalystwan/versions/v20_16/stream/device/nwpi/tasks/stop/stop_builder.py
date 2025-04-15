# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import TasksStopResponsePayload


class StopBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/tasks/stop
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, task_id: str, **kw) -> TasksStopResponsePayload:
        """
        Task Action - Stop
        POST /dataservice/stream/device/nwpi/tasks/stop/{taskId}

        :param task_id: taskId
        :returns: TasksStopResponsePayload
        """
        params = {
            "taskId": task_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/stream/device/nwpi/tasks/stop/{taskId}",
            return_type=TasksStopResponsePayload,
            params=params,
            **kw,
        )
