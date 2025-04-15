# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .application.application_builder import ApplicationBuilder
    from .applications.applications_builder import ApplicationsBuilder
    from .gatewayexits.gatewayexits_builder import GatewayexitsBuilder
    from .loadbalance.loadbalance_builder import LoadbalanceBuilder
    from .localexits.localexits_builder import LocalexitsBuilder


class CloudxBuilder:
    """
    Builds and executes requests for operations under /device/cloudx
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def application(self) -> ApplicationBuilder:
        """
        The application property
        """
        from .application.application_builder import ApplicationBuilder

        return ApplicationBuilder(self._request_adapter)

    @property
    def applications(self) -> ApplicationsBuilder:
        """
        The applications property
        """
        from .applications.applications_builder import ApplicationsBuilder

        return ApplicationsBuilder(self._request_adapter)

    @property
    def gatewayexits(self) -> GatewayexitsBuilder:
        """
        The gatewayexits property
        """
        from .gatewayexits.gatewayexits_builder import GatewayexitsBuilder

        return GatewayexitsBuilder(self._request_adapter)

    @property
    def loadbalance(self) -> LoadbalanceBuilder:
        """
        The loadbalance property
        """
        from .loadbalance.loadbalance_builder import LoadbalanceBuilder

        return LoadbalanceBuilder(self._request_adapter)

    @property
    def localexits(self) -> LocalexitsBuilder:
        """
        The localexits property
        """
        from .localexits.localexits_builder import LocalexitsBuilder

        return LocalexitsBuilder(self._request_adapter)
