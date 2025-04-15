# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .control.control_builder import ControlBuilder
    from .devicebringup.devicebringup_builder import DevicebringupBuilder


class TroubleshootingBuilder:
    """
    Builds and executes requests for operations under /troubleshooting
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def control(self) -> ControlBuilder:
        """
        The control property
        """
        from .control.control_builder import ControlBuilder

        return ControlBuilder(self._request_adapter)

    @property
    def devicebringup(self) -> DevicebringupBuilder:
        """
        The devicebringup property
        """
        from .devicebringup.devicebringup_builder import DevicebringupBuilder

        return DevicebringupBuilder(self._request_adapter)
