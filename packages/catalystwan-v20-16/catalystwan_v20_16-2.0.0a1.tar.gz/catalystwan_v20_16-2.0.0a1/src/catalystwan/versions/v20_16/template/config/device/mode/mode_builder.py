# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .cli.cli_builder import CliBuilder
    from .vmanage.vmanage_builder import VmanageBuilder


class ModeBuilder:
    """
    Builds and executes requests for operations under /template/config/device/mode
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
    def vmanage(self) -> VmanageBuilder:
        """
        The vmanage property
        """
        from .vmanage.vmanage_builder import VmanageBuilder

        return VmanageBuilder(self._request_adapter)
