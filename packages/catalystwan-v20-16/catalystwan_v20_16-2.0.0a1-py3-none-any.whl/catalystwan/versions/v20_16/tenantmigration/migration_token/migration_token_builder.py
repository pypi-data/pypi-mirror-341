# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class MigrationTokenBuilder:
    """
    Builds and executes requests for operations under /tenantmigration/migrationToken
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, migration_id: str, **kw) -> Any:
        """
        Get migration token
        GET /dataservice/tenantmigration/migrationToken

        :param migration_id: Migration Id
        :returns: Any
        """
        params = {
            "migrationId": migration_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/tenantmigration/migrationToken", params=params, **kw
        )
