# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .optin.optin_builder import OptinBuilder
    from .optout.optout_builder import OptoutBuilder


class TelemetryBuilder:
    """
    Builds and executes requests for operations under /cloudservices/telemetry
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get Telemetry state
        GET /dataservice/cloudservices/telemetry

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/cloudservices/telemetry", **kw)

    @property
    def optin(self) -> OptinBuilder:
        """
        The optin property
        """
        from .optin.optin_builder import OptinBuilder

        return OptinBuilder(self._request_adapter)

    @property
    def optout(self) -> OptoutBuilder:
        """
        The optout property
        """
        from .optout.optout_builder import OptoutBuilder

        return OptoutBuilder(self._request_adapter)
