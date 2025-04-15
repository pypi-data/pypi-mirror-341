# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .cybervision.cybervision_builder import CybervisionBuilder


class OtherBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/other
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def cybervision(self) -> CybervisionBuilder:
        """
        The cybervision property
        """
        from .cybervision.cybervision_builder import CybervisionBuilder

        return CybervisionBuilder(self._request_adapter)
