# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class RemotemepBuilder:
    """
    Builds and executes requests for operations under /device/cfm/mp/remotemep
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        domain: Optional[str] = None,
        service: Optional[str] = None,
        local_mep_id: Optional[int] = None,
        remote_mep_id: Optional[int] = None,
        **kw,
    ) -> Any:
        """
        Get mp remote mep from device
        GET /dataservice/device/cfm/mp/remotemep

        :param domain: Domain Name
        :param service: Service Name
        :param local_mep_id: Local MEP ID
        :param remote_mep_id: Remote MEP ID
        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "domain": domain,
            "service": service,
            "local-mep-id": local_mep_id,
            "remote-mep-id": remote_mep_id,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/cfm/mp/remotemep", params=params, **kw
        )
