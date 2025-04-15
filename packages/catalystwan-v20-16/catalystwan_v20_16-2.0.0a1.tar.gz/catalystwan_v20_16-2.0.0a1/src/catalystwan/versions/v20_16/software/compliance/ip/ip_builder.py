# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .origin.origin_builder import OriginBuilder


class IpBuilder:
    """
    Builds and executes requests for operations under /software/compliance/ip
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def origin(self) -> OriginBuilder:
        """
        The origin property
        """
        from .origin.origin_builder import OriginBuilder

        return OriginBuilder(self._request_adapter)
