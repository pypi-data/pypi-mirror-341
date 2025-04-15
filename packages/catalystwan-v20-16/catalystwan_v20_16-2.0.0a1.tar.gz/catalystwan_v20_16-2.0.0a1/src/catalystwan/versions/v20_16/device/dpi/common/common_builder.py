# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .applications.applications_builder import ApplicationsBuilder


class CommonBuilder:
    """
    Builds and executes requests for operations under /device/dpi/common
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def applications(self) -> ApplicationsBuilder:
        """
        The applications property
        """
        from .applications.applications_builder import ApplicationsBuilder

        return ApplicationsBuilder(self._request_adapter)
