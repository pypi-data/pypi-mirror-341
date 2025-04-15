# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class SizeBuilder:
    """
    Builds and executes requests for operations under /util/configdb/size
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Fetches the disk usage by configuration-db
        GET /dataservice/util/configdb/size

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/util/configdb/size", **kw)
