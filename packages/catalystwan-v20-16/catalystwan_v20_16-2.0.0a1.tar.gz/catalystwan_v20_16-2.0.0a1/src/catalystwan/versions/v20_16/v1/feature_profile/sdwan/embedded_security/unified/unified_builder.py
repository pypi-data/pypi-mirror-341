# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .ngfirewall.ngfirewall_builder import NgfirewallBuilder


class UnifiedBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/embedded-security/{securityId}/unified
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def ngfirewall(self) -> NgfirewallBuilder:
        """
        The ngfirewall property
        """
        from .ngfirewall.ngfirewall_builder import NgfirewallBuilder

        return NgfirewallBuilder(self._request_adapter)
