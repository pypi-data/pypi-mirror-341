# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class QosmosNbarMigrationWarningBuilder:
    """
    Builds and executes requests for operations under /template/policy/vsmart/qosmos_nbar_migration_warning
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Qosmos Nbar migration
        GET /dataservice/template/policy/vsmart/qosmos_nbar_migration_warning

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/template/policy/vsmart/qosmos_nbar_migration_warning", **kw
        )
