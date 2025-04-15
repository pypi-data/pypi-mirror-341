# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AccessCodeResponse


class AccesscodeBuilder:
    """
    Builds and executes requests for operations under /webex/accesscode
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> AccessCodeResponse:
        """
        Webex Access Code Details
        GET /dataservice/webex/accesscode

        :returns: AccessCodeResponse
        """
        return self._request_adapter.request(
            "GET", "/dataservice/webex/accesscode", return_type=AccessCodeResponse, **kw
        )
