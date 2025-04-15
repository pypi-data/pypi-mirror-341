# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeployTopologyGroupPostRequest, DeployTopologyGroupPostResponse


class DeployBuilder:
    """
    Builds and executes requests for operations under /v1/topology-group/{topologyGroupId}/device/deploy
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, topology_group_id: str, payload: DeployTopologyGroupPostRequest, **kw
    ) -> DeployTopologyGroupPostResponse:
        """
        deploy Topology group to devices
        POST /dataservice/v1/topology-group/{topologyGroupId}/device/deploy

        :param topology_group_id: Topology Group Id
        :param payload: Payload
        :returns: DeployTopologyGroupPostResponse
        """
        params = {
            "topologyGroupId": topology_group_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/topology-group/{topologyGroupId}/device/deploy",
            return_type=DeployTopologyGroupPostResponse,
            params=params,
            payload=payload,
            **kw,
        )
