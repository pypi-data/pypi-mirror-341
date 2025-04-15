# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface


class StatusBuilder:
    """
    Builds and executes requests for operations under /statistics/process/status
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, process_queue: Optional[int] = None, **kw) -> List[Any]:
        """
        Get stats process report
        GET /dataservice/statistics/process/status

        :param process_queue: Process queue
        :returns: List[Any]
        """
        params = {
            "processQueue": process_queue,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/process/status",
            return_type=List[Any],
            params=params,
            **kw,
        )
