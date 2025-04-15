# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class DownloadBuilder:
    """
    Builds and executes requests for operations under /v1/reports/{reportId}/tasks/{taskId}/download
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, report_id: str, task_id: str, **kw) -> str:
        """
        Download a report file
        GET /dataservice/v1/reports/{reportId}/tasks/{taskId}/download

        :param report_id: Report id
        :param task_id: Task id
        :returns: str
        """
        params = {
            "reportId": report_id,
            "taskId": task_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/reports/{reportId}/tasks/{taskId}/download",
            return_type=str,
            params=params,
            **kw,
        )
