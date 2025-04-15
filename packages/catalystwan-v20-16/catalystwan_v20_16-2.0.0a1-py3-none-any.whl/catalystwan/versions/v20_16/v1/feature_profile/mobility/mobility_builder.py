# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .cli.cli_builder import CliBuilder
    from .global_.global_builder import GlobalBuilder


class MobilityBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/mobility
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
    def global_(self) -> GlobalBuilder:
        """
        The global property
        """
        from .global_.global_builder import GlobalBuilder

        return GlobalBuilder(self._request_adapter)
