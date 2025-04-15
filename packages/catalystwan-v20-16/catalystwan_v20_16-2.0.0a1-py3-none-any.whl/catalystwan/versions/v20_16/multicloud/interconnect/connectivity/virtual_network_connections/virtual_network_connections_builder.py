# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InterconnectVirtualNetworkConnection, ProcessResponse


class VirtualNetworkConnectionsBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/connectivity/virtual-network-connections
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get_interconnect_virtual_network_connections(
        self,
        connection_name: Optional[str] = None,
        cloud_type: Optional[str] = None,
        cloud_account_id: Optional[str] = None,
        refresh: Optional[str] = "false",
        **kw,
    ) -> Any:
        """
        API to retrieve all exisiting Interconnect virtual network connections.
        GET /dataservice/multicloud/interconnect/connectivity/virtual-network-connections

        :param connection_name: Interconnect virtual cross connection name
        :param cloud_type: Cloud provider type
        :param cloud_account_id: Cloud account id
        :param refresh: Interconnect virtual network connection provider sync enabled
        :returns: Any
        """
        params = {
            "connection-name": connection_name,
            "cloud-type": cloud_type,
            "cloud-account-id": cloud_account_id,
            "refresh": refresh,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/connectivity/virtual-network-connections",
            params=params,
            **kw,
        )

    def post(self, payload: List[InterconnectVirtualNetworkConnection], **kw) -> ProcessResponse:
        """
        API to create a Interconnect virtual network connection between virtual network Tags and OnRamp gateway connection.
        POST /dataservice/multicloud/interconnect/connectivity/virtual-network-connections

        :param payload: Request Payload for Interconnect virtual network Connections
        :returns: ProcessResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/multicloud/interconnect/connectivity/virtual-network-connections",
            return_type=ProcessResponse,
            payload=payload,
            **kw,
        )

    def get(self, connection_name: str, **kw) -> InterconnectVirtualNetworkConnection:
        """
        API to retrieve an exisiting Interconnect Interconnect virtual network connection.
        GET /dataservice/multicloud/interconnect/connectivity/virtual-network-connections/{connection-name}

        :param connection_name: Interconnect virtual network connection name
        :returns: InterconnectVirtualNetworkConnection
        """
        params = {
            "connection-name": connection_name,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/connectivity/virtual-network-connections/{connection-name}",
            return_type=InterconnectVirtualNetworkConnection,
            params=params,
            **kw,
        )

    def put(
        self, connection_name: str, payload: InterconnectVirtualNetworkConnection, **kw
    ) -> ProcessResponse:
        """
        API to update a virtual network connection between virtual network Tags and onRamp gateway connection.
        PUT /dataservice/multicloud/interconnect/connectivity/virtual-network-connections/{connection-name}

        :param connection_name: Interconnect virtual network connection name
        :param payload: Request Payload for Interconnect virtual network connections
        :returns: ProcessResponse
        """
        params = {
            "connection-name": connection_name,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/multicloud/interconnect/connectivity/virtual-network-connections/{connection-name}",
            return_type=ProcessResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, connection_name: str, **kw) -> ProcessResponse:
        """
        API to delete an Interconnect virtual network connection.
        DELETE /dataservice/multicloud/interconnect/connectivity/virtual-network-connections/{connection-name}

        :param connection_name: Interconnect virtual cross connection name
        :returns: ProcessResponse
        """
        params = {
            "connection-name": connection_name,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/multicloud/interconnect/connectivity/virtual-network-connections/{connection-name}",
            return_type=ProcessResponse,
            params=params,
            **kw,
        )
