# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .current15minstats.current15_minstats_builder import Current15MinstatsBuilder
    from .totalstats.totalstats_builder import TotalstatsBuilder


class Voicet1E1ControllerinfoBuilder:
    """
    Builds and executes requests for operations under /device/voicet1e1controllerinfo
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def current15minstats(self) -> Current15MinstatsBuilder:
        """
        The current15minstats property
        """
        from .current15minstats.current15_minstats_builder import Current15MinstatsBuilder

        return Current15MinstatsBuilder(self._request_adapter)

    @property
    def totalstats(self) -> TotalstatsBuilder:
        """
        The totalstats property
        """
        from .totalstats.totalstats_builder import TotalstatsBuilder

        return TotalstatsBuilder(self._request_adapter)
