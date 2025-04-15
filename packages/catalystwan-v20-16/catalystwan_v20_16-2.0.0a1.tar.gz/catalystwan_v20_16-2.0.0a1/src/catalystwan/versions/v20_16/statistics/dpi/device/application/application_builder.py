# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .flowcount.flowcount_builder import FlowcountBuilder


class ApplicationBuilder:
    """
    Builds and executes requests for operations under /statistics/dpi/device/application
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def flowcount(self) -> FlowcountBuilder:
        """
        The flowcount property
        """
        from .flowcount.flowcount_builder import FlowcountBuilder

        return FlowcountBuilder(self._request_adapter)
