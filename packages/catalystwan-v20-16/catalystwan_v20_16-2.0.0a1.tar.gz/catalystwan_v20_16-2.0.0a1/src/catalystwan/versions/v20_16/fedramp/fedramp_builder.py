# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .dnssec.dnssec_builder import DnssecBuilder
    from .status.status_builder import StatusBuilder
    from .wazuh.wazuh_builder import WazuhBuilder


class FedrampBuilder:
    """
    Builds and executes requests for operations under /fedramp
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def dnssec(self) -> DnssecBuilder:
        """
        The dnssec property
        """
        from .dnssec.dnssec_builder import DnssecBuilder

        return DnssecBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)

    @property
    def wazuh(self) -> WazuhBuilder:
        """
        The wazuh property
        """
        from .wazuh.wazuh_builder import WazuhBuilder

        return WazuhBuilder(self._request_adapter)
