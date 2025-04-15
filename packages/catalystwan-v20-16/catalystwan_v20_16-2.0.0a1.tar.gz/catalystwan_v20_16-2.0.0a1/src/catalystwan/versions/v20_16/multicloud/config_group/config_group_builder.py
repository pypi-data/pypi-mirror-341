# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .topology.topology_builder import TopologyBuilder


class ConfigGroupBuilder:
    """
    Builds and executes requests for operations under /multicloud/{cloudType}/config-group
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def topology(self) -> TopologyBuilder:
        """
        The topology property
        """
        from .topology.topology_builder import TopologyBuilder

        return TopologyBuilder(self._request_adapter)
