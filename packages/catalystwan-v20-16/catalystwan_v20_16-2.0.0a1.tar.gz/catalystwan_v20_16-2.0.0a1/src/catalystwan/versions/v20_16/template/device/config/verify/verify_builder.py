# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ValidateTemplatePostRequest


class VerifyBuilder:
    """
    Builds and executes requests for operations under /template/device/config/verify
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: ValidateTemplatePostRequest, **kw):
        """
        Validate full template"



        Note: In a multitenant vManage system, this API is only available in the Provider view.
        POST /dataservice/template/device/config/verify

        :param payload: Payload
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "validateTemplate")
        return self._request_adapter.request(
            "POST", "/dataservice/template/device/config/verify", payload=payload, **kw
        )
