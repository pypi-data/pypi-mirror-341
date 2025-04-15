# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class OtpBuilder:
    """
    Builds and executes requests for operations under /dca/cloudservices/otp
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get cloud service OTP value
        GET /dataservice/dca/cloudservices/otp

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/dca/cloudservices/otp", **kw)

    def put(self, payload: Any, **kw):
        """
        Update cloud service OTP value
        PUT /dataservice/dca/cloudservices/otp

        :param payload: Cloud service OTP value
        :returns: None
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/dca/cloudservices/otp", payload=payload, **kw
        )
