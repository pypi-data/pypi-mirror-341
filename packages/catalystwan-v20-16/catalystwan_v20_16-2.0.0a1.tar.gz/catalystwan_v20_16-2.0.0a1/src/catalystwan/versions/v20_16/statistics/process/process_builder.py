# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .counters.counters_builder import CountersBuilder
    from .status.status_builder import StatusBuilder
    from .thread.thread_builder import ThreadBuilder


class ProcessBuilder:
    """
    Builds and executes requests for operations under /statistics/process
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Process stats data
        GET /dataservice/statistics/process

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/statistics/process", **kw)

    @property
    def counters(self) -> CountersBuilder:
        """
        The counters property
        """
        from .counters.counters_builder import CountersBuilder

        return CountersBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)

    @property
    def thread(self) -> ThreadBuilder:
        """
        The thread property
        """
        from .thread.thread_builder import ThreadBuilder

        return ThreadBuilder(self._request_adapter)
