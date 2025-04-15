# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class DetachBuilder:
    """
    Builds and executes requests for operations under /template/device/config/detach
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw):
        """
        Detach device template


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        POST /dataservice/template/device/config/detach

        :param payload: Device template
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "detachDeviceTemplate")
        return self._request_adapter.request(
            "POST", "/dataservice/template/device/config/detach", payload=payload, **kw
        )
