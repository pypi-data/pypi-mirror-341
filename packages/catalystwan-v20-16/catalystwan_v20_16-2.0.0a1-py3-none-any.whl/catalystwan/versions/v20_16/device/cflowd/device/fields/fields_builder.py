# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class FieldsBuilder:
    """
    Builds and executes requests for operations under /device/cflowd/device/fields
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, is_device_dash_board: Optional[bool] = False, **kw) -> Any:
        """
        Get CflowdvDPI query field JSON
        GET /dataservice/device/cflowd/device/fields

        :param is_device_dash_board: Flag whether it is device dashboard request
        :returns: Any
        """
        params = {
            "isDeviceDashBoard": is_device_dash_board,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/cflowd/device/fields", params=params, **kw
        )
