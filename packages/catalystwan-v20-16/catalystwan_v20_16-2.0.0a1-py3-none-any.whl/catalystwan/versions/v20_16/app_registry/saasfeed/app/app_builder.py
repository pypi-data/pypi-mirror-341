# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .configure.configure_builder import ConfigureBuilder


class AppBuilder:
    """
    Builds and executes requests for operations under /app-registry/saasfeed/app
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, feed_id: str, **kw) -> List[Any]:
        """
        Get All Saas feed details of a particular application
        GET /dataservice/app-registry/saasfeed/app/{feedId}

        :param feed_id: Feed ID
        :returns: List[Any]
        """
        params = {
            "feedId": feed_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/app-registry/saasfeed/app/{feedId}",
            return_type=List[Any],
            params=params,
            **kw,
        )

    @property
    def configure(self) -> ConfigureBuilder:
        """
        The configure property
        """
        from .configure.configure_builder import ConfigureBuilder

        return ConfigureBuilder(self._request_adapter)
