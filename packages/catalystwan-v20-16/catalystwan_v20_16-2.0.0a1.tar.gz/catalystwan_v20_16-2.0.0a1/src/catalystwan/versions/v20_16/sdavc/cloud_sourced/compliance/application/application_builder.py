# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import Application, ExtendedApplicationRequestData


class ApplicationBuilder:
    """
    Builds and executes requests for operations under /sdavc/cloud-sourced/compliance/application
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: ExtendedApplicationRequestData, **kw) -> Application:
        """
        Post
        POST /dataservice/sdavc/cloud-sourced/compliance/application

        :param payload: Payload
        :returns: Application
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/sdavc/cloud-sourced/compliance/application",
            return_type=Application,
            payload=payload,
            **kw,
        )
