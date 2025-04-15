# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .replicator.replicator_builder import ReplicatorBuilder
    from .rpf.rpf_builder import RpfBuilder
    from .topology.topology_builder import TopologyBuilder
    from .tunnel.tunnel_builder import TunnelBuilder


class MulticastBuilder:
    """
    Builds and executes requests for operations under /device/multicast
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def replicator(self) -> ReplicatorBuilder:
        """
        The replicator property
        """
        from .replicator.replicator_builder import ReplicatorBuilder

        return ReplicatorBuilder(self._request_adapter)

    @property
    def rpf(self) -> RpfBuilder:
        """
        The rpf property
        """
        from .rpf.rpf_builder import RpfBuilder

        return RpfBuilder(self._request_adapter)

    @property
    def topology(self) -> TopologyBuilder:
        """
        The topology property
        """
        from .topology.topology_builder import TopologyBuilder

        return TopologyBuilder(self._request_adapter)

    @property
    def tunnel(self) -> TunnelBuilder:
        """
        The tunnel property
        """
        from .tunnel.tunnel_builder import TunnelBuilder

        return TunnelBuilder(self._request_adapter)
