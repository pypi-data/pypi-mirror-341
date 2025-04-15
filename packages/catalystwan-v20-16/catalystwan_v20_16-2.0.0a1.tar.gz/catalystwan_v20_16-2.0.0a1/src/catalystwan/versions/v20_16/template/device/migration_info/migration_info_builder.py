# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class MigrationInfoBuilder:
    """
    Builds and executes requests for operations under /template/device/migration_info
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Returns the mapping between old and migrated templates


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/template/device/migration_info

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/template/device/migration_info", **kw
        )
