# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .app.app_builder import AppBuilder


class SaasfeedBuilder:
    """
    Builds and executes requests for operations under /app-registry/saasfeed
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get All Saas feed details
        GET /dataservice/app-registry/saasfeed

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/app-registry/saasfeed", return_type=List[Any], **kw
        )

    @property
    def app(self) -> AppBuilder:
        """
        The app property
        """
        from .app.app_builder import AppBuilder

        return AppBuilder(self._request_adapter)
