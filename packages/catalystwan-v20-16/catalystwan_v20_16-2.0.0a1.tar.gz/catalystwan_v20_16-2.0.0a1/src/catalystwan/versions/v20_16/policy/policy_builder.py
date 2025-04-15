# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .wani.wani_builder import WaniBuilder


class PolicyBuilder:
    """
    Builds and executes requests for operations under /policy
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def wani(self) -> WaniBuilder:
        """
        The wani property
        """
        from .wani.wani_builder import WaniBuilder

        return WaniBuilder(self._request_adapter)
