# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class CountBuilder:
    """
    Builds and executes requests for operations under /networkdesign/profile/task/count
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get device profile configuration task count
        GET /dataservice/networkdesign/profile/task/count

        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getDeviceProfileTaskCount")
        return self._request_adapter.request(
            "GET", "/dataservice/networkdesign/profile/task/count", **kw
        )
