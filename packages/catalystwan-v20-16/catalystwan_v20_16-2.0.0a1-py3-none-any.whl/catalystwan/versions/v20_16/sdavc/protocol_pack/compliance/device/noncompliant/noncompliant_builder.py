# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CompliantDeviceRequest


class NoncompliantBuilder:
    """
    Builds and executes requests for operations under /sdavc/protocol-pack/compliance/device/noncompliant
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: CompliantDeviceRequest, **kw) -> Any:
        """
        Get all non compliant devices for given protocol pack and selected device or entire network
        POST /dataservice/sdavc/protocol-pack/compliance/device/noncompliant

        :param payload: Request Payload
        :returns: Any
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/sdavc/protocol-pack/compliance/device/noncompliant",
            payload=payload,
            **kw,
        )

    def get(self, protocol_pack_name: str, **kw) -> Any:
        """
        Get all non compliant devices for given protocol pack
        GET /dataservice/sdavc/protocol-pack/compliance/device/noncompliant/{protocolPackName}

        :param protocol_pack_name: Protocol pack name
        :returns: Any
        """
        params = {
            "protocolPackName": protocol_pack_name,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/sdavc/protocol-pack/compliance/device/noncompliant/{protocolPackName}",
            params=params,
            **kw,
        )
