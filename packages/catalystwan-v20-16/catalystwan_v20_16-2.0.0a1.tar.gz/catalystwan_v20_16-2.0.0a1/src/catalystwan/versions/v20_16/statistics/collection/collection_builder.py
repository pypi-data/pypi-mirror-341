# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .reset.reset_builder import ResetBuilder


class CollectionBuilder:
    """
    Builds and executes requests for operations under /statistics/collection
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def reset(self) -> ResetBuilder:
        """
        The reset property
        """
        from .reset.reset_builder import ResetBuilder

        return ResetBuilder(self._request_adapter)
