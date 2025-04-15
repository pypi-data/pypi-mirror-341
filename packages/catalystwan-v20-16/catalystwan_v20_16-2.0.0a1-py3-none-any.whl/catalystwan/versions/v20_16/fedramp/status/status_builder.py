# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class StatusBuilder:
    """
    Builds and executes requests for operations under /fedramp/status
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw):
        """
        Set network deployment mode
        POST /dataservice/fedramp/status

        :param payload: Network deployment mode
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/fedramp/status", payload=payload, **kw
        )
