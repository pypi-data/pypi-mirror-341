# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class SettingsBuilder:
    """
    Builds and executes requests for operations under /util/olapdb/migration/settings
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get migration generic settings
        GET /dataservice/util/olapdb/migration/settings

        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getStatsMigrationSettings")
        return self._request_adapter.request(
            "GET", "/dataservice/util/olapdb/migration/settings", **kw
        )

    def post(self, payload: str, **kw) -> Any:
        """
        Config generic settings
        POST /dataservice/util/olapdb/migration/settings

        :param payload: generic settings
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "postStatsMigrationSettings")
        return self._request_adapter.request(
            "POST", "/dataservice/util/olapdb/migration/settings", payload=payload, **kw
        )
