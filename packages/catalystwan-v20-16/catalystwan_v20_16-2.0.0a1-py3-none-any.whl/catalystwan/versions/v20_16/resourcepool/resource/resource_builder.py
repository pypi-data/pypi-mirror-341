# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .vpn.vpn_builder import VpnBuilder


class ResourceBuilder:
    """
    Builds and executes requests for operations under /resourcepool/resource
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def vpn(self) -> VpnBuilder:
        """
        The vpn property
        """
        from .vpn.vpn_builder import VpnBuilder

        return VpnBuilder(self._request_adapter)
