# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .flow_count.flow_count_builder import FlowCountBuilder
    from .flows.flows_builder import FlowsBuilder


class LogBuilder:
    """
    Builds and executes requests for operations under /device/app/log
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def flow_count(self) -> FlowCountBuilder:
        """
        The flow-count property
        """
        from .flow_count.flow_count_builder import FlowCountBuilder

        return FlowCountBuilder(self._request_adapter)

    @property
    def flows(self) -> FlowsBuilder:
        """
        The flows property
        """
        from .flows.flows_builder import FlowsBuilder

        return FlowsBuilder(self._request_adapter)
