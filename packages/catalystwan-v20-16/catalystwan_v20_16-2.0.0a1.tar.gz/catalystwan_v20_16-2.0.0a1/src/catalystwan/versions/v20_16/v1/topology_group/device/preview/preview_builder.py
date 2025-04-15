# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    GetTopologyGroupDeviceConfigurationPreviewPostRequest,
    GetTopologyGroupDeviceConfigurationPreviewPostResponse,
)


class PreviewBuilder:
    """
    Builds and executes requests for operations under /v1/topology-group/{topologyGroupId}/device/{deviceId}/preview
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        topology_group_id: str,
        device_id: str,
        payload: GetTopologyGroupDeviceConfigurationPreviewPostRequest,
        **kw,
    ) -> GetTopologyGroupDeviceConfigurationPreviewPostResponse:
        """
        Get a preview of the configuration for a device
        POST /dataservice/v1/topology-group/{topologyGroupId}/device/{deviceId}/preview

        :param topology_group_id: Topology Group Id
        :param device_id: Device Id
        :param payload: Payload
        :returns: GetTopologyGroupDeviceConfigurationPreviewPostResponse
        """
        params = {
            "topologyGroupId": topology_group_id,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/topology-group/{topologyGroupId}/device/{deviceId}/preview",
            return_type=GetTopologyGroupDeviceConfigurationPreviewPostResponse,
            params=params,
            payload=payload,
            **kw,
        )
