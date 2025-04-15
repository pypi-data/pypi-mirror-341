# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .clear.clear_builder import ClearBuilder


class SessionsBuilder:
    """
    Builds and executes requests for operations under /stream/device/log/sessions
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw):
        """
        Get
        GET /dataservice/stream/device/log/sessions

        :returns: None
        """
        return self._request_adapter.request("GET", "/dataservice/stream/device/log/sessions", **kw)

    @property
    def clear(self) -> ClearBuilder:
        """
        The clear property
        """
        from .clear.clear_builder import ClearBuilder

        return ClearBuilder(self._request_adapter)
