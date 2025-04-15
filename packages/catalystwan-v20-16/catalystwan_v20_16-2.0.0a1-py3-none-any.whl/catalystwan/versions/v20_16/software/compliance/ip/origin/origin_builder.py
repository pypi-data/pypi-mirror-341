# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .check.check_builder import CheckBuilder


class OriginBuilder:
    """
    Builds and executes requests for operations under /software/compliance/ip/origin
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def check(self) -> CheckBuilder:
        """
        The check property
        """
        from .check.check_builder import CheckBuilder

        return CheckBuilder(self._request_adapter)
