# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class SupportedCommandsBuilder:
    """
    Builds and executes requests for operations under /device/file-based/data-collection/supported-commands
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_uuid: str, **kw) -> str:
        """
        Get Supported Command list for given Device UUID
        GET /dataservice/device/file-based/data-collection/supported-commands/{deviceUUID}

        :param device_uuid: Device UUID
        :returns: str
        """
        params = {
            "deviceUUID": device_uuid,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/file-based/data-collection/supported-commands/{deviceUUID}",
            return_type=str,
            params=params,
            **kw,
        )
