# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .heatmap.heatmap_builder import HeatmapBuilder
    from .site.site_builder import SiteBuilder
    from .sites.sites_builder import SitesBuilder


class ApplicationBuilder:
    """
    Builds and executes requests for operations under /statistics/perfmon/application
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def heatmap(self) -> HeatmapBuilder:
        """
        The heatmap property
        """
        from .heatmap.heatmap_builder import HeatmapBuilder

        return HeatmapBuilder(self._request_adapter)

    @property
    def site(self) -> SiteBuilder:
        """
        The site property
        """
        from .site.site_builder import SiteBuilder

        return SiteBuilder(self._request_adapter)

    @property
    def sites(self) -> SitesBuilder:
        """
        The sites property
        """
        from .sites.sites_builder import SitesBuilder

        return SitesBuilder(self._request_adapter)
