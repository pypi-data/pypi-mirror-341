# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class InitiateDeviceComplianceBuilder:
    """
    Builds and executes requests for operations under /sdavc/protocol-pack/compliance/initiate-device-compliance
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, **kw) -> Any:
        """
        Initiate device compliance task
        POST /dataservice/sdavc/protocol-pack/compliance/initiate-device-compliance

        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/sdavc/protocol-pack/compliance/initiate-device-compliance", **kw
        )
