# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ImportBuilder:
    """
    Builds and executes requests for operations under /restore/import
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, **kw) -> Any:
        """
        Submit a previously backed up file and import the data and apply it to the configuraion database
        POST /dataservice/restore/import

        :returns: Any
        """
        return self._request_adapter.request("POST", "/dataservice/restore/import", **kw)
