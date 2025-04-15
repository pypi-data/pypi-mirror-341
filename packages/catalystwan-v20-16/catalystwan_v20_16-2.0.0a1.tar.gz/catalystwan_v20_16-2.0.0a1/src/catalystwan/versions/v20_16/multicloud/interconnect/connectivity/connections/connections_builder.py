# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .tags.tags_builder import TagsBuilder


class ConnectionsBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/connectivity/connections
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def tags(self) -> TagsBuilder:
        """
        The tags property
        """
        from .tags.tags_builder import TagsBuilder

        return TagsBuilder(self._request_adapter)
