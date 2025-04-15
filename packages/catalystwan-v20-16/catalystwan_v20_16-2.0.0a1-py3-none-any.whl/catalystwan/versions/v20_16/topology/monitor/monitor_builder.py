# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .site.site_builder import SiteBuilder


class MonitorBuilder:
    """
    Builds and executes requests for operations under /topology/monitor
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def site(self) -> SiteBuilder:
        """
        The site property
        """
        from .site.site_builder import SiteBuilder

        return SiteBuilder(self._request_adapter)
