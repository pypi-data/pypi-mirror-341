# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .common.common_builder import CommonBuilder
    from .dmvpn.dmvpn_builder import DmvpnBuilder


class CryptovpnBuilder:
    """
    Builds and executes requests for operations under /statistics/cryptovpn
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def common(self) -> CommonBuilder:
        """
        The common property
        """
        from .common.common_builder import CommonBuilder

        return CommonBuilder(self._request_adapter)

    @property
    def dmvpn(self) -> DmvpnBuilder:
        """
        The dmvpn property
        """
        from .dmvpn.dmvpn_builder import DmvpnBuilder

        return DmvpnBuilder(self._request_adapter)
