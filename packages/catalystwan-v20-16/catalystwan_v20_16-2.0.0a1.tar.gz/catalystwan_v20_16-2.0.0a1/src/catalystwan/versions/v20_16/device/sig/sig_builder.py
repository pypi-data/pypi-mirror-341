# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .get_sig_tunnel_list.get_sig_tunnel_list_builder import GetSigTunnelListBuilder
    from .get_sig_tunnel_total.get_sig_tunnel_total_builder import GetSigTunnelTotalBuilder
    from .tunnel_dashboard.tunnel_dashboard_builder import TunnelDashboardBuilder
    from .umbrella.umbrella_builder import UmbrellaBuilder
    from .zscaler.zscaler_builder import ZscalerBuilder


class SigBuilder:
    """
    Builds and executes requests for operations under /device/sig
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def get_sig_tunnel_list(self) -> GetSigTunnelListBuilder:
        """
        The getSigTunnelList property
        """
        from .get_sig_tunnel_list.get_sig_tunnel_list_builder import GetSigTunnelListBuilder

        return GetSigTunnelListBuilder(self._request_adapter)

    @property
    def get_sig_tunnel_total(self) -> GetSigTunnelTotalBuilder:
        """
        The getSigTunnelTotal property
        """
        from .get_sig_tunnel_total.get_sig_tunnel_total_builder import GetSigTunnelTotalBuilder

        return GetSigTunnelTotalBuilder(self._request_adapter)

    @property
    def tunnel_dashboard(self) -> TunnelDashboardBuilder:
        """
        The tunnelDashboard property
        """
        from .tunnel_dashboard.tunnel_dashboard_builder import TunnelDashboardBuilder

        return TunnelDashboardBuilder(self._request_adapter)

    @property
    def umbrella(self) -> UmbrellaBuilder:
        """
        The umbrella property
        """
        from .umbrella.umbrella_builder import UmbrellaBuilder

        return UmbrellaBuilder(self._request_adapter)

    @property
    def zscaler(self) -> ZscalerBuilder:
        """
        The zscaler property
        """
        from .zscaler.zscaler_builder import ZscalerBuilder

        return ZscalerBuilder(self._request_adapter)
