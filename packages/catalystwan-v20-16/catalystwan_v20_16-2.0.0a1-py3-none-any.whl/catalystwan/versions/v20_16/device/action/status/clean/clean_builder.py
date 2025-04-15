# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Optional

from catalystwan.abc import RequestAdapterInterface


class CleanBuilder:
    """
    Builds and executes requests for operations under /device/action/status/clean
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, clean_status: Optional[bool] = None, **kw):
        """
        Delete task and status vertex
        GET /dataservice/device/action/status/clean

        :param clean_status: Clean status
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "cleanStatus")
        params = {
            "cleanStatus": clean_status,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/action/status/clean", params=params, **kw
        )
