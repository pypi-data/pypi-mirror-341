# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface


class UnsupportedCliConfigBuilder:
    """
    Builds and executes requests for operations under /v1/device/unsupportedCliConfig
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_uuid: str, highlight_unsupported_clis: Optional[bool] = True, **kw) -> str:
        """
        Get Unsupported CLI Config for device
        GET /dataservice/v1/device/unsupportedCliConfig/{deviceUUID}

        :param device_uuid: Device uuid
        :param highlight_unsupported_clis: Highlight unsupported clis
        :returns: str
        """
        params = {
            "deviceUUID": device_uuid,
            "highlightUnsupportedClis": highlight_unsupported_clis,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/device/unsupportedCliConfig/{deviceUUID}",
            return_type=str,
            params=params,
            **kw,
        )
