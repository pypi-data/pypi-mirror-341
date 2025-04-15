# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .license.license_builder import LicenseBuilder


class VaBuilder:
    """
    Builds and executes requests for operations under /msla/va
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def license(self) -> LicenseBuilder:
        """
        The License property
        """
        from .license.license_builder import LicenseBuilder

        return LicenseBuilder(self._request_adapter)
