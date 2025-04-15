# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .cloud.cloud_builder import CloudBuilder
    from .map.map_builder import MapBuilder
    from .sync.sync_builder import SyncBuilder
    from .wanrg.wanrg_builder import WanrgBuilder


class CortexBuilder:
    """
    Builds and executes requests for operations under /template/cortex
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get Cortex List
        GET /dataservice/template/cortex

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/template/cortex", return_type=List[Any], **kw
        )

    @property
    def cloud(self) -> CloudBuilder:
        """
        The cloud property
        """
        from .cloud.cloud_builder import CloudBuilder

        return CloudBuilder(self._request_adapter)

    @property
    def map(self) -> MapBuilder:
        """
        The map property
        """
        from .map.map_builder import MapBuilder

        return MapBuilder(self._request_adapter)

    @property
    def sync(self) -> SyncBuilder:
        """
        The sync property
        """
        from .sync.sync_builder import SyncBuilder

        return SyncBuilder(self._request_adapter)

    @property
    def wanrg(self) -> WanrgBuilder:
        """
        The wanrg property
        """
        from .wanrg.wanrg_builder import WanrgBuilder

        return WanrgBuilder(self._request_adapter)
