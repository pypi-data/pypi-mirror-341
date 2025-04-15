# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ParametersBuilder:
    """
    Builds and executes requests for operations under /networkdesign/global/parameters
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get global parameter templates
        GET /dataservice/networkdesign/global/parameters

        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getGlobalParameters")
        return self._request_adapter.request(
            "GET", "/dataservice/networkdesign/global/parameters", **kw
        )
