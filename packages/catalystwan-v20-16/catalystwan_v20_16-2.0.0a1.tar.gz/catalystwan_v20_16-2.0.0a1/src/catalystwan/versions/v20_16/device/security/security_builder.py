# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .information.information_builder import InformationBuilder


class SecurityBuilder:
    """
    Builds and executes requests for operations under /device/security
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def information(self) -> InformationBuilder:
        """
        The information property
        """
        from .information.information_builder import InformationBuilder

        return InformationBuilder(self._request_adapter)
