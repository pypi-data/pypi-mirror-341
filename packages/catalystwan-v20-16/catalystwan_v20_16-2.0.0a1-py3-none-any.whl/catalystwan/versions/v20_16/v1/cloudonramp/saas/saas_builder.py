# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .cloud_tunnels.cloud_tunnels_builder import CloudTunnelsBuilder
    from .configuration.configuration_builder import ConfigurationBuilder
    from .devices.devices_builder import DevicesBuilder
    from .inactivesites.inactivesites_builder import InactivesitesBuilder
    from .legacydevicelist.legacydevicelist_builder import LegacydevicelistBuilder
    from .status.status_builder import StatusBuilder
    from .webexsyncstatus.webexsyncstatus_builder import WebexsyncstatusBuilder


class SaasBuilder:
    """
    Builds and executes requests for operations under /v1/cloudonramp/saas
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw):
        """
        Get Cloud On Ramp For Saas apps status
        GET /dataservice/v1/cloudonramp/saas

        :returns: None
        """
        return self._request_adapter.request("GET", "/dataservice/v1/cloudonramp/saas", **kw)

    @property
    def cloud_tunnels(self) -> CloudTunnelsBuilder:
        """
        The cloud_tunnels property
        """
        from .cloud_tunnels.cloud_tunnels_builder import CloudTunnelsBuilder

        return CloudTunnelsBuilder(self._request_adapter)

    @property
    def configuration(self) -> ConfigurationBuilder:
        """
        The configuration property
        """
        from .configuration.configuration_builder import ConfigurationBuilder

        return ConfigurationBuilder(self._request_adapter)

    @property
    def devices(self) -> DevicesBuilder:
        """
        The devices property
        """
        from .devices.devices_builder import DevicesBuilder

        return DevicesBuilder(self._request_adapter)

    @property
    def inactivesites(self) -> InactivesitesBuilder:
        """
        The inactivesites property
        """
        from .inactivesites.inactivesites_builder import InactivesitesBuilder

        return InactivesitesBuilder(self._request_adapter)

    @property
    def legacydevicelist(self) -> LegacydevicelistBuilder:
        """
        The legacydevicelist property
        """
        from .legacydevicelist.legacydevicelist_builder import LegacydevicelistBuilder

        return LegacydevicelistBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)

    @property
    def webexsyncstatus(self) -> WebexsyncstatusBuilder:
        """
        The webexsyncstatus property
        """
        from .webexsyncstatus.webexsyncstatus_builder import WebexsyncstatusBuilder

        return WebexsyncstatusBuilder(self._request_adapter)
