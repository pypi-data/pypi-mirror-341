# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .dca.dca_builder import DcaBuilder


class AnalyticsBuilder:
    """
    Builds and executes requests for operations under /settings/configuration/analytics
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def dca(self) -> DcaBuilder:
        """
        The dca property
        """
        from .dca.dca_builder import DcaBuilder

        return DcaBuilder(self._request_adapter)
