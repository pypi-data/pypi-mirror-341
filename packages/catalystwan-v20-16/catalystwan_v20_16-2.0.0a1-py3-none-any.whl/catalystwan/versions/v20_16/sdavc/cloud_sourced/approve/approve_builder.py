# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DefaultSuccessResponse, ExtendedApplicationRequestData


class ApproveBuilder:
    """
    Builds and executes requests for operations under /sdavc/cloud-sourced/approve
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: ExtendedApplicationRequestData, **kw) -> DefaultSuccessResponse:
        """
        Post
        POST /dataservice/sdavc/cloud-sourced/approve

        :param payload: Payload
        :returns: DefaultSuccessResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/sdavc/cloud-sourced/approve",
            return_type=DefaultSuccessResponse,
            payload=payload,
            **kw,
        )
