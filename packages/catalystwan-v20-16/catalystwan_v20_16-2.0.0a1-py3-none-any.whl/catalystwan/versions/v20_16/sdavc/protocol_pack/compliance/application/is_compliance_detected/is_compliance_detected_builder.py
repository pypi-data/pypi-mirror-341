# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class IsComplianceDetectedBuilder:
    """
    Builds and executes requests for operations under /sdavc/protocol-pack/compliance/application/is-compliance-detected
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Check if there is any Application Compliance detected in the system
        GET /dataservice/sdavc/protocol-pack/compliance/application/is-compliance-detected

        :returns: Any
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/sdavc/protocol-pack/compliance/application/is-compliance-detected",
            **kw,
        )
