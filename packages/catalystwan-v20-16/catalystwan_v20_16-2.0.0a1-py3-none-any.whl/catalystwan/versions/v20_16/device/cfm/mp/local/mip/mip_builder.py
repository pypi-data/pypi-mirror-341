# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class MipBuilder:
    """
    Builds and executes requests for operations under /device/cfm/mp/local/mip
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        level: Optional[int] = None,
        port: Optional[str] = None,
        svc_inst: Optional[int] = None,
        **kw,
    ) -> Any:
        """
        Get mp local mip from device
        GET /dataservice/device/cfm/mp/local/mip

        :param level: Level
        :param port: Port
        :param svc_inst: Service Instance
        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "level": level,
            "port": port,
            "svc-inst": svc_inst,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/cfm/mp/local/mip", params=params, **kw
        )
