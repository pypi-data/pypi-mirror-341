# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .upgrade.upgrade_builder import UpgradeBuilder


class ZtpBuilder:
    """
    Builds and executes requests for operations under /device/action/ztp
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def upgrade(self) -> UpgradeBuilder:
        """
        The upgrade property
        """
        from .upgrade.upgrade_builder import UpgradeBuilder

        return UpgradeBuilder(self._request_adapter)
