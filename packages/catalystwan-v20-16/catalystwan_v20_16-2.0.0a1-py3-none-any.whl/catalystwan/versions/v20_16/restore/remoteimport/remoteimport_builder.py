# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class RemoteimportBuilder:
    """
    Builds and executes requests for operations under /restore/remoteimport
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Remote import backup from a remote URL and import the data and apply it to the configuraion database
        POST /dataservice/restore/remoteimport

        :param payload: ImportBackupInfo Payload
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/restore/remoteimport", payload=payload, **kw
        )
