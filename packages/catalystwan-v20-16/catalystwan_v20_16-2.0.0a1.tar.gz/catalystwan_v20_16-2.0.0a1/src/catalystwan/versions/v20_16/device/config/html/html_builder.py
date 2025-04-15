# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import List

from catalystwan.abc import RequestAdapterInterface


class HtmlBuilder:
    """
    Builds and executes requests for operations under /device/config/html
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: List[str], **kw) -> str:
        """
        Get device running configuration in HTML format
        GET /dataservice/device/config/html

        :param device_id: Device Id list
        :returns: str
        """
        logging.warning("Operation: %s is deprecated", "getDeviceRunningConfigHTML")
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/config/html", return_type=str, params=params, **kw
        )
