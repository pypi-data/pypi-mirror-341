# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class TypeBuilder:
    """
    Builds and executes requests for operations under /stream/device/log/type
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, uuid: str, **kw):
        """
        Get
        GET /dataservice/stream/device/log/type

        :param uuid: Device uuid
        :returns: None
        """
        params = {
            "uuid": uuid,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/stream/device/log/type", params=params, **kw
        )
