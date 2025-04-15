# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .connection.connection_builder import ConnectionBuilder
    from .counter.counter_builder import CounterBuilder
    from .data_usage.data_usage_builder import DataUsageBuilder
    from .details.details_builder import DetailsBuilder
    from .hardware.hardware_builder import HardwareBuilder
    from .health.health_builder import HealthBuilder
    from .modem.modem_builder import ModemBuilder
    from .network.network_builder import NetworkBuilder
    from .profiles.profiles_builder import ProfilesBuilder
    from .radio.radio_builder import RadioBuilder
    from .sessions.sessions_builder import SessionsBuilder
    from .status.status_builder import StatusBuilder


class CellularBuilder:
    """
    Builds and executes requests for operations under /device/cellular
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def connection(self) -> ConnectionBuilder:
        """
        The connection property
        """
        from .connection.connection_builder import ConnectionBuilder

        return ConnectionBuilder(self._request_adapter)

    @property
    def counter(self) -> CounterBuilder:
        """
        The counter property
        """
        from .counter.counter_builder import CounterBuilder

        return CounterBuilder(self._request_adapter)

    @property
    def data_usage(self) -> DataUsageBuilder:
        """
        The dataUsage property
        """
        from .data_usage.data_usage_builder import DataUsageBuilder

        return DataUsageBuilder(self._request_adapter)

    @property
    def details(self) -> DetailsBuilder:
        """
        The details property
        """
        from .details.details_builder import DetailsBuilder

        return DetailsBuilder(self._request_adapter)

    @property
    def hardware(self) -> HardwareBuilder:
        """
        The hardware property
        """
        from .hardware.hardware_builder import HardwareBuilder

        return HardwareBuilder(self._request_adapter)

    @property
    def health(self) -> HealthBuilder:
        """
        The health property
        """
        from .health.health_builder import HealthBuilder

        return HealthBuilder(self._request_adapter)

    @property
    def modem(self) -> ModemBuilder:
        """
        The modem property
        """
        from .modem.modem_builder import ModemBuilder

        return ModemBuilder(self._request_adapter)

    @property
    def network(self) -> NetworkBuilder:
        """
        The network property
        """
        from .network.network_builder import NetworkBuilder

        return NetworkBuilder(self._request_adapter)

    @property
    def profiles(self) -> ProfilesBuilder:
        """
        The profiles property
        """
        from .profiles.profiles_builder import ProfilesBuilder

        return ProfilesBuilder(self._request_adapter)

    @property
    def radio(self) -> RadioBuilder:
        """
        The radio property
        """
        from .radio.radio_builder import RadioBuilder

        return RadioBuilder(self._request_adapter)

    @property
    def sessions(self) -> SessionsBuilder:
        """
        The sessions property
        """
        from .sessions.sessions_builder import SessionsBuilder

        return SessionsBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)
