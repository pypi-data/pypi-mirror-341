# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .cli.cli_builder import CliBuilder
    from .networks.networks_builder import NetworksBuilder
    from .system.system_builder import SystemBuilder


class NfvirtualBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/nfvirtual
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def cli(self) -> CliBuilder:
        """
        The cli property
        """
        from .cli.cli_builder import CliBuilder

        return CliBuilder(self._request_adapter)

    @property
    def networks(self) -> NetworksBuilder:
        """
        The networks property
        """
        from .networks.networks_builder import NetworksBuilder

        return NetworksBuilder(self._request_adapter)

    @property
    def system(self) -> SystemBuilder:
        """
        The system property
        """
        from .system.system_builder import SystemBuilder

        return SystemBuilder(self._request_adapter)
