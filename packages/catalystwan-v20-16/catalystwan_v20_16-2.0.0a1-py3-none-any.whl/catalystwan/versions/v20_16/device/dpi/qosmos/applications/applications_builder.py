# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class ApplicationsBuilder:
    """
    Builds and executes requests for operations under /device/dpi/qosmos/applications
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get DPI QoSMos application list from device
        GET /dataservice/device/dpi/qosmos/applications

        :returns: List[Any]
        """
        logging.warning("Operation: %s is deprecated", "getQosmosApplicationList")
        return self._request_adapter.request(
            "GET", "/dataservice/device/dpi/qosmos/applications", return_type=List[Any], **kw
        )
