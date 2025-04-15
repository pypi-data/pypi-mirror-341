# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EnrollOtpResponse, EnrollOtpSettings


class ServerBuilder:
    """
    Builds and executes requests for operations under /cdna/server
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> EnrollOtpResponse:
        """
        Get CDNA Server Details
        GET /dataservice/cdna/server

        :returns: EnrollOtpResponse
        """
        return self._request_adapter.request(
            "GET", "/dataservice/cdna/server", return_type=EnrollOtpResponse, **kw
        )

    def put(self, payload: EnrollOtpSettings, **kw) -> EnrollOtpResponse:
        """
        Enroll CDNA Server with OTP
        PUT /dataservice/cdna/server

        :param payload: CDNA OTP Details
        :returns: EnrollOtpResponse
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/cdna/server", return_type=EnrollOtpResponse, payload=payload, **kw
        )

    def delete(self, **kw):
        """
        Delete CDNA Server Details
        DELETE /dataservice/cdna/server

        :returns: None
        """
        return self._request_adapter.request("DELETE", "/dataservice/cdna/server", **kw)
