# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InterconnectCrossConnection, ProcessResponse


class VirtualCrossConnectionsBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/connectivity/virtual-cross-connections
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get_interconnect_cross_connections(
        self,
        interconnect_type: Optional[str] = None,
        interconnect_gateway_name: Optional[str] = None,
        connection_name: Optional[str] = None,
        connection_type: Optional[str] = None,
        cloud_type: Optional[str] = None,
        refresh: Optional[str] = "false",
        **kw,
    ) -> Any:
        """
        API to retrieve all exisiting Interconnect virtual cross connections.
        GET /dataservice/multicloud/interconnect/connectivity/virtual-cross-connections

        :param interconnect_type: Interconnect provider Type
        :param interconnect_gateway_name: Interconnect gateway name
        :param connection_name: Interconnect virtual cross connection name
        :param connection_type: Interconnect virtual cross connection type
        :param cloud_type: Cloud provider type
        :param refresh: Interconnect connection provider sync enabled
        :returns: Any
        """
        params = {
            "interconnect-type": interconnect_type,
            "interconnect-gateway-name": interconnect_gateway_name,
            "connection-name": connection_name,
            "connection-type": connection_type,
            "cloud-type": cloud_type,
            "refresh": refresh,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/connectivity/virtual-cross-connections",
            params=params,
            **kw,
        )

    def post(self, payload: List[InterconnectCrossConnection], **kw) -> ProcessResponse:
        """
        API to create an Interconnect virtual cross connection on an Interconnect Gateway at an Interconnect Provider.
        POST /dataservice/multicloud/interconnect/connectivity/virtual-cross-connections

        :param payload: Request Payload for Interconnect virtual cross connections
        :returns: ProcessResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/multicloud/interconnect/connectivity/virtual-cross-connections",
            return_type=ProcessResponse,
            payload=payload,
            **kw,
        )

    def get(self, connection_name: str, **kw) -> Any:
        """
        API to retrieve an exisiting Interconnect virtual cross connection.
        GET /dataservice/multicloud/interconnect/connectivity/virtual-cross-connections/{connection-name}

        :param connection_name: Interconnect virtual cross connection name
        :returns: Any
        """
        params = {
            "connection-name": connection_name,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/connectivity/virtual-cross-connections/{connection-name}",
            params=params,
            **kw,
        )

    def put(
        self, connection_name: str, payload: InterconnectCrossConnection, **kw
    ) -> ProcessResponse:
        """
        API to update a virtual cross connection connection on an Interconnect Gateway at an Interconnect Provider.
        PUT /dataservice/multicloud/interconnect/connectivity/virtual-cross-connections/{connection-name}

        :param connection_name: Interconnect virtual cross connection name
        :param payload: Request Payload for Multicloud Interconnect Virtual Cross Connections
        :returns: ProcessResponse
        """
        params = {
            "connection-name": connection_name,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/multicloud/interconnect/connectivity/virtual-cross-connections/{connection-name}",
            return_type=ProcessResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, connection_name: str, **kw) -> ProcessResponse:
        """
        API to delete an Interconnect virtual cross connection at an Interconnect provider.
        DELETE /dataservice/multicloud/interconnect/connectivity/virtual-cross-connections/{connection-name}

        :param connection_name: Interconnect virtual cross connection name
        :returns: ProcessResponse
        """
        params = {
            "connection-name": connection_name,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/multicloud/interconnect/connectivity/virtual-cross-connections/{connection-name}",
            return_type=ProcessResponse,
            params=params,
            **kw,
        )
