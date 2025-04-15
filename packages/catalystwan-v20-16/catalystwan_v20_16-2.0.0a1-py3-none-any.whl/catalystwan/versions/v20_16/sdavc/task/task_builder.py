# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class TaskBuilder:
    """
    Builds and executes requests for operations under /sdavc/task
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, task_id: str, payload: Any, **kw):
        """
        Activate container
        POST /dataservice/sdavc/task/{taskId}

        :param task_id: Task Id
        :param payload: Container task config
        :returns: None
        """
        params = {
            "taskId": task_id,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/sdavc/task/{taskId}", params=params, payload=payload, **kw
        )
