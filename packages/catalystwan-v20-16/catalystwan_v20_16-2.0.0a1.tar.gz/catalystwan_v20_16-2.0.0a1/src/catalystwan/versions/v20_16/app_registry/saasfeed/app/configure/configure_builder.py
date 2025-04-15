# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ConfigureBuilder:
    """
    Builds and executes requests for operations under /app-registry/saasfeed/app/configure
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, payload: Any, **kw) -> Any:
        """
        Get All the App for the given conditions
        PUT /dataservice/app-registry/saasfeed/app/configure

        :param payload: Onboard
        :returns: Any
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/app-registry/saasfeed/app/configure", payload=payload, **kw
        )
