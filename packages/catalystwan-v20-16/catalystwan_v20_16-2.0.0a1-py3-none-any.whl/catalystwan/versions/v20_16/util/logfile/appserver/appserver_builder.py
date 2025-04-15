# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .lastnlines.lastnlines_builder import LastnlinesBuilder


class AppserverBuilder:
    """
    Builds and executes requests for operations under /util/logfile/appserver
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Lists content of log file. This API accepts content type as text/plain. It is mandatory to provide response content type. Any other content type would result in empty response.
        GET /dataservice/util/logfile/appserver

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/util/logfile/appserver", **kw)

    @property
    def lastnlines(self) -> LastnlinesBuilder:
        """
        The lastnlines property
        """
        from .lastnlines.lastnlines_builder import LastnlinesBuilder

        return LastnlinesBuilder(self._request_adapter)
