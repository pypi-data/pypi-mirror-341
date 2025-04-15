# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .wanedge.wanedge_builder import WanedgeBuilder


class CertificateBuilder:
    """
    Builds and executes requests for operations under /sslproxy/certificate
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> Any:
        """
        Get edge proxy certificate
        GET /dataservice/sslproxy/certificate

        :param device_id: Device Id
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/sslproxy/certificate", params=params, **kw
        )

    def put(self, payload: Any, **kw) -> Any:
        """
        Upload device certificate
        PUT /dataservice/sslproxy/certificate

        :param payload: Upload device certificate
        :returns: Any
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/sslproxy/certificate", payload=payload, **kw
        )

    @property
    def wanedge(self) -> WanedgeBuilder:
        """
        The wanedge property
        """
        from .wanedge.wanedge_builder import WanedgeBuilder

        return WanedgeBuilder(self._request_adapter)
