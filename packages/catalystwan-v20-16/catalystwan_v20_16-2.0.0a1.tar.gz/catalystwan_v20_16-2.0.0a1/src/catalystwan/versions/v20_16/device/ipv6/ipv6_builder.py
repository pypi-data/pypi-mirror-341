# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .nd6.nd6_builder import Nd6Builder


class Ipv6Builder:
    """
    Builds and executes requests for operations under /device/ipv6
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def nd6(self) -> Nd6Builder:
        """
        The nd6 property
        """
        from .nd6.nd6_builder import Nd6Builder

        return Nd6Builder(self._request_adapter)
