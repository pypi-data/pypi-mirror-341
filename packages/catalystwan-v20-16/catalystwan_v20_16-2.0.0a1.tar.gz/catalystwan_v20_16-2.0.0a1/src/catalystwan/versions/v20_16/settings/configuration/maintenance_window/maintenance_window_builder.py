# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class MaintenanceWindowBuilder:
    """
    Builds and executes requests for operations under /settings/configuration/maintenanceWindow
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> str:
        """
        Retrieve maintenance window
        GET /dataservice/settings/configuration/maintenanceWindow

        :returns: str
        """
        return self._request_adapter.request(
            "GET", "/dataservice/settings/configuration/maintenanceWindow", return_type=str, **kw
        )
