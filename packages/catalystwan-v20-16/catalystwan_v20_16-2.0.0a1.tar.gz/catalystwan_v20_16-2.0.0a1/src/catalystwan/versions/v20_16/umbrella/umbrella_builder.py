# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .getkeys.getkeys_builder import GetkeysBuilder
    from .syncnow.syncnow_builder import SyncnowBuilder


class UmbrellaBuilder:
    """
    Builds and executes requests for operations under /umbrella
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def getkeys(self) -> GetkeysBuilder:
        """
        The getkeys property
        """
        from .getkeys.getkeys_builder import GetkeysBuilder

        return GetkeysBuilder(self._request_adapter)

    @property
    def syncnow(self) -> SyncnowBuilder:
        """
        The syncnow property
        """
        from .syncnow.syncnow_builder import SyncnowBuilder

        return SyncnowBuilder(self._request_adapter)
