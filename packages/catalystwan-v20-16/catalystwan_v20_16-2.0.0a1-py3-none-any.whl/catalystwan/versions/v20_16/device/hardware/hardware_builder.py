# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .alarms.alarms_builder import AlarmsBuilder
    from .environment.environment_builder import EnvironmentBuilder
    from .errors.errors_builder import ErrorsBuilder
    from .inventory.inventory_builder import InventoryBuilder
    from .status.status_builder import StatusBuilder
    from .synced.synced_builder import SyncedBuilder
    from .system.system_builder import SystemBuilder
    from .threshold.threshold_builder import ThresholdBuilder


class HardwareBuilder:
    """
    Builds and executes requests for operations under /device/hardware
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def alarms(self) -> AlarmsBuilder:
        """
        The alarms property
        """
        from .alarms.alarms_builder import AlarmsBuilder

        return AlarmsBuilder(self._request_adapter)

    @property
    def environment(self) -> EnvironmentBuilder:
        """
        The environment property
        """
        from .environment.environment_builder import EnvironmentBuilder

        return EnvironmentBuilder(self._request_adapter)

    @property
    def errors(self) -> ErrorsBuilder:
        """
        The errors property
        """
        from .errors.errors_builder import ErrorsBuilder

        return ErrorsBuilder(self._request_adapter)

    @property
    def inventory(self) -> InventoryBuilder:
        """
        The inventory property
        """
        from .inventory.inventory_builder import InventoryBuilder

        return InventoryBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)

    @property
    def synced(self) -> SyncedBuilder:
        """
        The synced property
        """
        from .synced.synced_builder import SyncedBuilder

        return SyncedBuilder(self._request_adapter)

    @property
    def system(self) -> SystemBuilder:
        """
        The system property
        """
        from .system.system_builder import SystemBuilder

        return SystemBuilder(self._request_adapter)

    @property
    def threshold(self) -> ThresholdBuilder:
        """
        The threshold property
        """
        from .threshold.threshold_builder import ThresholdBuilder

        return ThresholdBuilder(self._request_adapter)
