# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .queue.queue_builder import QueueBuilder


class OnDemandBuilder:
    """
    Builds and executes requests for operations under /statistics/on-demand
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def queue(self) -> QueueBuilder:
        """
        The queue property
        """
        from .queue.queue_builder import QueueBuilder

        return QueueBuilder(self._request_adapter)
