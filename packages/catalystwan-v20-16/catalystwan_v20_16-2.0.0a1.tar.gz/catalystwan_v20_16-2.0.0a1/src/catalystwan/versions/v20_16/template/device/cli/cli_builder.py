# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class CliBuilder:
    """
    Builds and executes requests for operations under /template/device/cli
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Create CLI template


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        POST /dataservice/template/device/cli

        :param payload: Create template request
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/template/device/cli", payload=payload, **kw
        )
