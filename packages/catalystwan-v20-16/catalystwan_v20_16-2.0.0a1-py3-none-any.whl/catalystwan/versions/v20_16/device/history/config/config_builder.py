# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, overload

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .diff.diff_builder import DiffBuilder


class ConfigBuilder:
    """
    Builds and executes requests for operations under /device/history/config
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @overload
    def get(self, *, device_id: str, query: str, **kw) -> Any:
        """
        Get device config history
        GET /dataservice/device/history/config

        :param device_id: Device Id
        :param query: Query filter
        :returns: Any
        """
        ...

    @overload
    def get(self, *, config_id: str, **kw) -> Any:
        """
        Get device config
        GET /dataservice/device/history/config/{config_id}

        :param config_id: Config Id
        :returns: Any
        """
        ...

    def get(
        self,
        *,
        device_id: Optional[str] = None,
        query: Optional[str] = None,
        config_id: Optional[str] = None,
        **kw,
    ) -> Any:
        # /dataservice/device/history/config
        if self._request_adapter.param_checker([(device_id, str), (query, str)], [config_id]):
            params = {
                "deviceId": device_id,
                "query": query,
            }
            return self._request_adapter.request(
                "GET", "/dataservice/device/history/config", params=params, **kw
            )
        # /dataservice/device/history/config/{config_id}
        if self._request_adapter.param_checker([(config_id, str)], [device_id, query]):
            params = {
                "config_id": config_id,
            }
            return self._request_adapter.request(
                "GET", "/dataservice/device/history/config/{config_id}", params=params, **kw
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def diff(self) -> DiffBuilder:
        """
        The diff property
        """
        from .diff.diff_builder import DiffBuilder

        return DiffBuilder(self._request_adapter)
