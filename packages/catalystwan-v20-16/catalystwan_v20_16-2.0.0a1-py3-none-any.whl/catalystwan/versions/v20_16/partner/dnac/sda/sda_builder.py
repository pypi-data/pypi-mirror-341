# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .config.config_builder import ConfigBuilder
    from .device.device_builder import DeviceBuilder
    from .netconfconfig.netconfconfig_builder import NetconfconfigBuilder
    from .site.site_builder import SiteBuilder
    from .vpn.vpn_builder import VpnBuilder


class SdaBuilder:
    """
    Builds and executes requests for operations under /partner/dnac/sda
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def config(self) -> ConfigBuilder:
        """
        The config property
        """
        from .config.config_builder import ConfigBuilder

        return ConfigBuilder(self._request_adapter)

    @property
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)

    @property
    def netconfconfig(self) -> NetconfconfigBuilder:
        """
        The netconfconfig property
        """
        from .netconfconfig.netconfconfig_builder import NetconfconfigBuilder

        return NetconfconfigBuilder(self._request_adapter)

    @property
    def site(self) -> SiteBuilder:
        """
        The site property
        """
        from .site.site_builder import SiteBuilder

        return SiteBuilder(self._request_adapter)

    @property
    def vpn(self) -> VpnBuilder:
        """
        The vpn property
        """
        from .vpn.vpn_builder import VpnBuilder

        return VpnBuilder(self._request_adapter)
