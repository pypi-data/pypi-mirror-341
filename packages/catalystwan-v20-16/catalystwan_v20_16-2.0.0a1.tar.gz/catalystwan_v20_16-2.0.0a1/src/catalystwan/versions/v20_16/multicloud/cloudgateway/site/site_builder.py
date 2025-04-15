# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    AttachSitesRequestPayloadInner,
    DetachSitesRequestPayloadInner,
    GetSitesResponse,
    Taskid,
    TunnelScalingRequestPayload,
)


class SiteBuilder:
    """
    Builds and executes requests for operations under /multicloud/cloudgateway/{cloudGatewayName}/site
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        cloud_gateway_name: str,
        system_ip: Optional[str] = None,
        site_id: Optional[str] = None,
        color: Optional[str] = None,
        vpn_tunnel_status: Optional[str] = None,
        solution: Optional[str] = None,
        **kw,
    ) -> GetSitesResponse:
        """
        Get sites attached to CGW
        GET /dataservice/multicloud/cloudgateway/{cloudGatewayName}/site

        :param cloud_gateway_name: Name of Cloud Gateway to attach site
        :param system_ip: System Ip of Branch Device
        :param site_id: Site Id
        :param color: color
        :param vpn_tunnel_status: Tunnel status of device
        :param solution: Solution of branch device
        :returns: GetSitesResponse
        """
        params = {
            "cloudGatewayName": cloud_gateway_name,
            "systemIp": system_ip,
            "siteId": site_id,
            "color": color,
            "vpnTunnelStatus": vpn_tunnel_status,
            "solution": solution,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/cloudgateway/{cloudGatewayName}/site",
            return_type=GetSitesResponse,
            params=params,
            **kw,
        )

    def put(self, cloud_gateway_name: str, payload: TunnelScalingRequestPayload, **kw) -> Taskid:
        """
        Update tunnel scaling and accelerated vpn parameter for a branch endpoint
        PUT /dataservice/multicloud/cloudgateway/{cloudGatewayName}/site

        :param cloud_gateway_name: Name of Cloud Gateway to attach site
        :param payload: Site Information
        :returns: Taskid
        """
        params = {
            "cloudGatewayName": cloud_gateway_name,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/multicloud/cloudgateway/{cloudGatewayName}/site",
            return_type=Taskid,
            params=params,
            payload=payload,
            **kw,
        )

    def post(
        self, cloud_gateway_name: str, payload: List[AttachSitesRequestPayloadInner], **kw
    ) -> Taskid:
        """
        Attach sites to Cloud Gateway
        POST /dataservice/multicloud/cloudgateway/{cloudGatewayName}/site

        :param cloud_gateway_name: Name of Cloud Gateway to attach site
        :param payload: Site Information
        :returns: Taskid
        """
        params = {
            "cloudGatewayName": cloud_gateway_name,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/multicloud/cloudgateway/{cloudGatewayName}/site",
            return_type=Taskid,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(
        self,
        cloud_gateway_name: str,
        payload: Optional[List[DetachSitesRequestPayloadInner]] = None,
        **kw,
    ) -> Taskid:
        """
        Detach sites from cloud gateway
        DELETE /dataservice/multicloud/cloudgateway/{cloudGatewayName}/site

        :param cloud_gateway_name: Name of Cloud Gateway to attach site
        :param payload: Site Information
        :returns: Taskid
        """
        params = {
            "cloudGatewayName": cloud_gateway_name,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/multicloud/cloudgateway/{cloudGatewayName}/site",
            return_type=Taskid,
            params=params,
            payload=payload,
            **kw,
        )
