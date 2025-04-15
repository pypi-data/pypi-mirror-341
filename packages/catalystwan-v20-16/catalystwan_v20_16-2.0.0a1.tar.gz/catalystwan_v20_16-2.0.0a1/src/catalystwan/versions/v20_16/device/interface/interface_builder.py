# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AfTypeParam, IfnameParam

if TYPE_CHECKING:
    from .arp_stats.arp_stats_builder import ArpStatsBuilder
    from .error_stats.error_stats_builder import ErrorStatsBuilder
    from .ipv6_stats.ipv6_stats_builder import Ipv6StatsBuilder
    from .pkt_size.pkt_size_builder import PktSizeBuilder
    from .port_stats.port_stats_builder import PortStatsBuilder
    from .qos_stats.qos_stats_builder import QosStatsBuilder
    from .queue_stats.queue_stats_builder import QueueStatsBuilder
    from .serial.serial_builder import SerialBuilder
    from .stats.stats_builder import StatsBuilder
    from .synced.synced_builder import SyncedBuilder
    from .trustsec.trustsec_builder import TrustsecBuilder
    from .vpn.vpn_builder import VpnBuilder


class InterfaceBuilder:
    """
    Builds and executes requests for operations under /device/interface
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        vpn_id: Optional[str] = None,
        ifname: Optional[IfnameParam] = None,
        af_type: Optional[AfTypeParam] = None,
        **kw,
    ) -> Any:
        """
        Get device interfaces
        GET /dataservice/device/interface

        :param vpn_id: VPN Id
        :param ifname: IF Name
        :param af_type: AF Type
        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "vpn-id": vpn_id,
            "ifname": ifname,
            "af-type": af_type,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/interface", params=params, **kw
        )

    @property
    def arp_stats(self) -> ArpStatsBuilder:
        """
        The arp_stats property
        """
        from .arp_stats.arp_stats_builder import ArpStatsBuilder

        return ArpStatsBuilder(self._request_adapter)

    @property
    def error_stats(self) -> ErrorStatsBuilder:
        """
        The error_stats property
        """
        from .error_stats.error_stats_builder import ErrorStatsBuilder

        return ErrorStatsBuilder(self._request_adapter)

    @property
    def ipv6_stats(self) -> Ipv6StatsBuilder:
        """
        The ipv6Stats property
        """
        from .ipv6_stats.ipv6_stats_builder import Ipv6StatsBuilder

        return Ipv6StatsBuilder(self._request_adapter)

    @property
    def pkt_size(self) -> PktSizeBuilder:
        """
        The pkt_size property
        """
        from .pkt_size.pkt_size_builder import PktSizeBuilder

        return PktSizeBuilder(self._request_adapter)

    @property
    def port_stats(self) -> PortStatsBuilder:
        """
        The port_stats property
        """
        from .port_stats.port_stats_builder import PortStatsBuilder

        return PortStatsBuilder(self._request_adapter)

    @property
    def qos_stats(self) -> QosStatsBuilder:
        """
        The qosStats property
        """
        from .qos_stats.qos_stats_builder import QosStatsBuilder

        return QosStatsBuilder(self._request_adapter)

    @property
    def queue_stats(self) -> QueueStatsBuilder:
        """
        The queue_stats property
        """
        from .queue_stats.queue_stats_builder import QueueStatsBuilder

        return QueueStatsBuilder(self._request_adapter)

    @property
    def serial(self) -> SerialBuilder:
        """
        The serial property
        """
        from .serial.serial_builder import SerialBuilder

        return SerialBuilder(self._request_adapter)

    @property
    def stats(self) -> StatsBuilder:
        """
        The stats property
        """
        from .stats.stats_builder import StatsBuilder

        return StatsBuilder(self._request_adapter)

    @property
    def synced(self) -> SyncedBuilder:
        """
        The synced property
        """
        from .synced.synced_builder import SyncedBuilder

        return SyncedBuilder(self._request_adapter)

    @property
    def trustsec(self) -> TrustsecBuilder:
        """
        The trustsec property
        """
        from .trustsec.trustsec_builder import TrustsecBuilder

        return TrustsecBuilder(self._request_adapter)

    @property
    def vpn(self) -> VpnBuilder:
        """
        The vpn property
        """
        from .vpn.vpn_builder import VpnBuilder

        return VpnBuilder(self._request_adapter)
