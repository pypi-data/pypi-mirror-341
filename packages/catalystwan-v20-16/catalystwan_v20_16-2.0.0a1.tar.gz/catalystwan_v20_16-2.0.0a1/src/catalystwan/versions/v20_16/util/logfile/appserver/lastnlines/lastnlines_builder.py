# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class LastnlinesBuilder:
    """
    Builds and executes requests for operations under /util/logfile/appserver/lastnlines
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, lines: Optional[int] = 100, **kw) -> Any:
        """
        List last N lines of log file. This API accepts content type as text/plain. It is mandatory to provide response content type. Any other content type would result in empty response.
        GET /dataservice/util/logfile/appserver/lastnlines

        :param lines: Lines
        :returns: Any
        """
        params = {
            "lines": lines,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/util/logfile/appserver/lastnlines", params=params, **kw
        )
