# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateInterconnectOnRampGatewayConnectionPostRequest,
    InterconnectOnRampGatewayConnection,
    ProcessResponse,
    UpdateInterconnectOnRampGatewayConnectionPutRequest,
)


class CloudOnrampGatewayConnectionsBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/connectivity/cloud-onramp-gateway-connections
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get_interconnect_on_ramp_gateway_connections(
        self,
        cloud_type: Optional[str] = None,
        cloud_account_id: Optional[str] = None,
        connection_name: Optional[str] = None,
        refresh: Optional[str] = "false",
        **kw,
    ) -> Any:
        """
        API to retrieve all Interconnect OnRamp gateway connection.
        GET /dataservice/multicloud/interconnect/connectivity/cloud-onramp-gateway-connections

        :param cloud_type: Cloud provider type
        :param cloud_account_id: Cloud account id
        :param connection_name: Interconnect OnRamp gateway connection name
        :param refresh: Interconnect connection provider sync enabled
        :returns: Any
        """
        params = {
            "cloud-type": cloud_type,
            "cloud-account-id": cloud_account_id,
            "connection-name": connection_name,
            "refresh": refresh,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/connectivity/cloud-onramp-gateway-connections",
            params=params,
            **kw,
        )

    def post(
        self, payload: List[CreateInterconnectOnRampGatewayConnectionPostRequest], **kw
    ) -> List[InterconnectOnRampGatewayConnection]:
        """
        API to create an Interconnect OnRamp gateway connection.
        POST /dataservice/multicloud/interconnect/connectivity/cloud-onramp-gateway-connections

        :param payload: Request payload for Interconnect OnRamp gateway connection
        :returns: List[InterconnectOnRampGatewayConnection]
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/multicloud/interconnect/connectivity/cloud-onramp-gateway-connections",
            return_type=List[InterconnectOnRampGatewayConnection],
            payload=payload,
            **kw,
        )

    def get(self, connection_name: str, **kw) -> InterconnectOnRampGatewayConnection:
        """
        API to retrieve a specific Interconnect OnRamp gateway connection.
        GET /dataservice/multicloud/interconnect/connectivity/cloud-onramp-gateway-connections/{connection-name}

        :param connection_name: Interconnect OnRamp gateway connection name
        :returns: InterconnectOnRampGatewayConnection
        """
        params = {
            "connection-name": connection_name,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/connectivity/cloud-onramp-gateway-connections/{connection-name}",
            return_type=InterconnectOnRampGatewayConnection,
            params=params,
            **kw,
        )

    def put(
        self,
        connection_name: str,
        payload: UpdateInterconnectOnRampGatewayConnectionPutRequest,
        **kw,
    ) -> ProcessResponse:
        """
        API to update an Interconnect OnRamp gateway connection.
        PUT /dataservice/multicloud/interconnect/connectivity/cloud-onramp-gateway-connections/{connection-name}

        :param connection_name: Interconnect OnRamp gateway connection name
        :param payload: Request payload for Interconnect OnRamp gateway connection
        :returns: ProcessResponse
        """
        params = {
            "connection-name": connection_name,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/multicloud/interconnect/connectivity/cloud-onramp-gateway-connections/{connection-name}",
            return_type=ProcessResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(
        self, connection_name: str, delete_cloud_resources: Optional[str] = "false", **kw
    ) -> ProcessResponse:
        """
        API to delete an Interconnect OnRamp gateway connection.
        DELETE /dataservice/multicloud/interconnect/connectivity/cloud-onramp-gateway-connections/{connection-name}

        :param connection_name: Interconnect OnRamp gateway connection name
        :param delete_cloud_resources: Interconnect connection provider sync enabled
        :returns: ProcessResponse
        """
        params = {
            "connection-name": connection_name,
            "delete-cloud-resources": delete_cloud_resources,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/multicloud/interconnect/connectivity/cloud-onramp-gateway-connections/{connection-name}",
            return_type=ProcessResponse,
            params=params,
            **kw,
        )
