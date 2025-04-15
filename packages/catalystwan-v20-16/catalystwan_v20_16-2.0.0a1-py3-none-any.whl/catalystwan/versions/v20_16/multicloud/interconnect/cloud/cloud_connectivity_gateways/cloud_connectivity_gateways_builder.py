# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CloudConnectivityGateway,
    CloudTypeParam,
    ConnectivityGatewayTypeParam,
    InlineResponse2008,
    InterconnectTypeParam,
)

if TYPE_CHECKING:
    from .create_options.create_options_builder import CreateOptionsBuilder


class CloudConnectivityGatewaysBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/cloud/{cloud-type}/cloud-connectivity-gateways
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        cloud_type: CloudTypeParam,
        cloud_account_id: str,
        connectivity_gateway_name: Optional[str] = None,
        connectivity_gateway_type: Optional[ConnectivityGatewayTypeParam] = None,
        interconnect_type: Optional[InterconnectTypeParam] = None,
        region: Optional[str] = None,
        network: Optional[str] = None,
        resource_state: Optional[str] = None,
        refresh: Optional[str] = "false",
        **kw,
    ) -> InlineResponse2008:
        """
        API to retrieve all Cloud Connectivity Gateways.
        GET /dataservice/multicloud/interconnect/cloud/{cloud-type}/cloud-connectivity-gateways

        :param cloud_type: Cloud Provider Type
        :param cloud_account_id: Cloud account id
        :param connectivity_gateway_name: Connectivity gateway name
        :param connectivity_gateway_type: Cloud Connectivity Gateway Type
        :param interconnect_type: Interconnect Provider Type
        :param region: Region
        :param network: Network
        :param resource_state: resource state
        :param refresh: Refresh
        :returns: InlineResponse2008
        """
        params = {
            "cloud-type": cloud_type,
            "cloud-account-id": cloud_account_id,
            "connectivity-gateway-name": connectivity_gateway_name,
            "connectivity-gateway-type": connectivity_gateway_type,
            "interconnect-type": interconnect_type,
            "region": region,
            "network": network,
            "resource-state": resource_state,
            "refresh": refresh,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/cloud/{cloud-type}/cloud-connectivity-gateways",
            return_type=InlineResponse2008,
            params=params,
            **kw,
        )

    def post(self, cloud_type: CloudTypeParam, payload: CloudConnectivityGateway, **kw) -> Any:
        """
        API to create a Cloud Connectivity Gateway such as Direct Connect Gateway, Express Route Circuit or Google Cloud routers.
        POST /dataservice/multicloud/interconnect/cloud/{cloud-type}/cloud-connectivity-gateways

        :param cloud_type: Cloud Provider Type
        :param payload: Request Payload for Multicloud Interconnect Cloud Connectivity Gateways
        :returns: Any
        """
        params = {
            "cloud-type": cloud_type,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/multicloud/interconnect/cloud/{cloud-type}/cloud-connectivity-gateways",
            params=params,
            payload=payload,
            **kw,
        )

    @overload
    def delete(
        self,
        *,
        connectivity_gateway_name: str,
        cloud_type: CloudTypeParam,
        connectivity_gateway_type: Optional[ConnectivityGatewayTypeParam] = None,
        **kw,
    ) -> Any:
        """
        API to delete a Cloud Connectivity Gateway.
        DELETE /dataservice/multicloud/interconnect/cloud/{cloud-type}/cloud-connectivity-gateways/{connectivity-gateway-name}

        :param connectivity_gateway_name: Connectivity gateway name
        :param cloud_type: Cloud Provider Type
        :param connectivity_gateway_type: Cloud Connectivity Gateway Type
        :returns: Any
        """
        ...

    @overload
    def delete(
        self,
        *,
        cloud_type: CloudTypeParam,
        connectivity_gateway_type: Optional[ConnectivityGatewayTypeParam] = None,
        **kw,
    ) -> Any:
        """
        API to delete Cloud Connectivity Gateways by type.
        DELETE /dataservice/multicloud/interconnect/cloud/{cloud-type}/cloud-connectivity-gateways

        :param cloud_type: Cloud Provider Type
        :param connectivity_gateway_type: Cloud Connectivity Gateway Type
        :returns: Any
        """
        ...

    def delete(
        self,
        *,
        cloud_type: CloudTypeParam,
        connectivity_gateway_type: Optional[ConnectivityGatewayTypeParam] = None,
        connectivity_gateway_name: Optional[str] = None,
        **kw,
    ) -> Any:
        # /dataservice/multicloud/interconnect/cloud/{cloud-type}/cloud-connectivity-gateways/{connectivity-gateway-name}
        if self._request_adapter.param_checker(
            [(connectivity_gateway_name, str), (cloud_type, CloudTypeParam)], []
        ):
            params = {
                "connectivity-gateway-name": connectivity_gateway_name,
                "cloud-type": cloud_type,
                "connectivity-gateway-type": connectivity_gateway_type,
            }
            return self._request_adapter.request(
                "DELETE",
                "/dataservice/multicloud/interconnect/cloud/{cloud-type}/cloud-connectivity-gateways/{connectivity-gateway-name}",
                params=params,
                **kw,
            )
        # /dataservice/multicloud/interconnect/cloud/{cloud-type}/cloud-connectivity-gateways
        if self._request_adapter.param_checker(
            [(cloud_type, CloudTypeParam)], [connectivity_gateway_name]
        ):
            params = {
                "cloud-type": cloud_type,
                "connectivity-gateway-type": connectivity_gateway_type,
            }
            return self._request_adapter.request(
                "DELETE",
                "/dataservice/multicloud/interconnect/cloud/{cloud-type}/cloud-connectivity-gateways",
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def create_options(self) -> CreateOptionsBuilder:
        """
        The create-options property
        """
        from .create_options.create_options_builder import CreateOptionsBuilder

        return CreateOptionsBuilder(self._request_adapter)
