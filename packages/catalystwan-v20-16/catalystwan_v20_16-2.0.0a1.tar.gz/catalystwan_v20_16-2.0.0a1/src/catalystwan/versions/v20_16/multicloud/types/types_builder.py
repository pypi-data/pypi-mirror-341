# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .edge.edge_builder import EdgeBuilder


class TypesBuilder:
    """
    Builds and executes requests for operations under /multicloud/types
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Obtain all supported Cloud Service Provider (CSP) types
        GET /dataservice/multicloud/types

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/multicloud/types", **kw)

    @property
    def edge(self) -> EdgeBuilder:
        """
        The edge property
        """
        from .edge.edge_builder import EdgeBuilder

        return EdgeBuilder(self._request_adapter)
