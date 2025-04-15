# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .bfd_statistics.bfd_statistics_builder import BfdStatisticsBuilder
    from .fec_statistics.fec_statistics_builder import FecStatisticsBuilder
    from .gre_keepalives.gre_keepalives_builder import GreKeepalivesBuilder
    from .ipsec_statistics.ipsec_statistics_builder import IpsecStatisticsBuilder
    from .packet_duplicate.packet_duplicate_builder import PacketDuplicateBuilder
    from .statistics.statistics_builder import StatisticsBuilder


class TunnelBuilder:
    """
    Builds and executes requests for operations under /device/tunnel
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def bfd_statistics(self) -> BfdStatisticsBuilder:
        """
        The bfd_statistics property
        """
        from .bfd_statistics.bfd_statistics_builder import BfdStatisticsBuilder

        return BfdStatisticsBuilder(self._request_adapter)

    @property
    def fec_statistics(self) -> FecStatisticsBuilder:
        """
        The fec_statistics property
        """
        from .fec_statistics.fec_statistics_builder import FecStatisticsBuilder

        return FecStatisticsBuilder(self._request_adapter)

    @property
    def gre_keepalives(self) -> GreKeepalivesBuilder:
        """
        The gre-keepalives property
        """
        from .gre_keepalives.gre_keepalives_builder import GreKeepalivesBuilder

        return GreKeepalivesBuilder(self._request_adapter)

    @property
    def ipsec_statistics(self) -> IpsecStatisticsBuilder:
        """
        The ipsec_statistics property
        """
        from .ipsec_statistics.ipsec_statistics_builder import IpsecStatisticsBuilder

        return IpsecStatisticsBuilder(self._request_adapter)

    @property
    def packet_duplicate(self) -> PacketDuplicateBuilder:
        """
        The packet-duplicate property
        """
        from .packet_duplicate.packet_duplicate_builder import PacketDuplicateBuilder

        return PacketDuplicateBuilder(self._request_adapter)

    @property
    def statistics(self) -> StatisticsBuilder:
        """
        The statistics property
        """
        from .statistics.statistics_builder import StatisticsBuilder

        return StatisticsBuilder(self._request_adapter)
