# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class DownloadBuilder:
    """
    Builds and executes requests for operations under /device/file-based/data-collection/download
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, request_uuid: str, **kw):
        """
        Download generated file
        GET /dataservice/device/file-based/data-collection/download/{requestUUID}

        :param request_uuid: request UUID
        :returns: None
        """
        params = {
            "requestUUID": request_uuid,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/file-based/data-collection/download/{requestUUID}",
            params=params,
            **kw,
        )
