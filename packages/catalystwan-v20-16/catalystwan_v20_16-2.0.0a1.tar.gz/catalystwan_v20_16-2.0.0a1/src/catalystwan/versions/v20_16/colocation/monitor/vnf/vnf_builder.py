# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .action.action_builder import ActionBuilder
    from .alarms.alarms_builder import AlarmsBuilder
    from .events.events_builder import EventsBuilder
    from .interface.interface_builder import InterfaceBuilder


class VnfBuilder:
    """
    Builds and executes requests for operations under /colocation/monitor/vnf
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def action(self) -> ActionBuilder:
        """
        The action property
        """
        from .action.action_builder import ActionBuilder

        return ActionBuilder(self._request_adapter)

    @property
    def alarms(self) -> AlarmsBuilder:
        """
        The alarms property
        """
        from .alarms.alarms_builder import AlarmsBuilder

        return AlarmsBuilder(self._request_adapter)

    @property
    def events(self) -> EventsBuilder:
        """
        The events property
        """
        from .events.events_builder import EventsBuilder

        return EventsBuilder(self._request_adapter)

    @property
    def interface(self) -> InterfaceBuilder:
        """
        The interface property
        """
        from .interface.interface_builder import InterfaceBuilder

        return InterfaceBuilder(self._request_adapter)
