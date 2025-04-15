# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class GetUserSettingsBuilder:
    """
    Builds and executes requests for operations under /smartLicensing/getUserSettings
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        get settings
        GET /dataservice/smartLicensing/getUserSettings

        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "get settings")
        return self._request_adapter.request(
            "GET", "/dataservice/smartLicensing/getUserSettings", **kw
        )
