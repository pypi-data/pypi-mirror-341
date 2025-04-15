# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class NetworkMigrationBuilder:
    """
    Builds and executes requests for operations under /tenantmigration/networkMigration
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Re-trigger network migration
        GET /dataservice/tenantmigration/networkMigration

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/tenantmigration/networkMigration", **kw
        )

    def post(self, payload: Any, **kw) -> Any:
        """
        Migrate network
        POST /dataservice/tenantmigration/networkMigration

        :param payload: Network migration
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/tenantmigration/networkMigration", payload=payload, **kw
        )
