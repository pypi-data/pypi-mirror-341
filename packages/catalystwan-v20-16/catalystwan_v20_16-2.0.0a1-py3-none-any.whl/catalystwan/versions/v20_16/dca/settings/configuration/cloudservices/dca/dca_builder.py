# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class DcaBuilder:
    """
    Builds and executes requests for operations under /dca/settings/configuration/cloudservices/dca
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get DCA cloud service configuration
        GET /dataservice/dca/settings/configuration/cloudservices/dca

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/dca/settings/configuration/cloudservices/dca", **kw
        )
