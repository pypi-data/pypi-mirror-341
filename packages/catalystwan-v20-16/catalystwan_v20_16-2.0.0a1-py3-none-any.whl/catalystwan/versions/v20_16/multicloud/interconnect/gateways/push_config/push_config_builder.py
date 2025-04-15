# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GatewaysPushconfigBody, ProcessResponse


class PushConfigBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/gateways/push-config
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: GatewaysPushconfigBody, **kw) -> ProcessResponse:
        """
        API to initiate a configuration push for an Interconnect gateway.
        POST /dataservice/multicloud/interconnect/gateways/push-config

        :param payload: Request Payload for Multicloud Interconnect Gateway Configuration Push
        :returns: ProcessResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/multicloud/interconnect/gateways/push-config",
            return_type=ProcessResponse,
            payload=payload,
            **kw,
        )
