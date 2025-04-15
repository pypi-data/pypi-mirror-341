# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ReportTaskQueryResponse, TaskIdResponse

if TYPE_CHECKING:
    from .download.download_builder import DownloadBuilder


class TasksBuilder:
    """
    Builds and executes requests for operations under /v1/reports/{reportId}/tasks
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, report_id: str, **kw) -> ReportTaskQueryResponse:
        """
        Get all report task detail information by report ID
        GET /dataservice/v1/reports/{reportId}/tasks

        :param report_id: Report id
        :returns: ReportTaskQueryResponse
        """
        params = {
            "reportId": report_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/reports/{reportId}/tasks",
            return_type=ReportTaskQueryResponse,
            params=params,
            **kw,
        )

    def delete(self, report_id: str, task_id: str, **kw) -> TaskIdResponse:
        """
        Delete the report task file by task ID
        DELETE /dataservice/v1/reports/{reportId}/tasks/{taskId}

        :param report_id: Report id
        :param task_id: Task id
        :returns: TaskIdResponse
        """
        params = {
            "reportId": report_id,
            "taskId": task_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/reports/{reportId}/tasks/{taskId}",
            return_type=TaskIdResponse,
            params=params,
            **kw,
        )

    @property
    def download(self) -> DownloadBuilder:
        """
        The download property
        """
        from .download.download_builder import DownloadBuilder

        return DownloadBuilder(self._request_adapter)
