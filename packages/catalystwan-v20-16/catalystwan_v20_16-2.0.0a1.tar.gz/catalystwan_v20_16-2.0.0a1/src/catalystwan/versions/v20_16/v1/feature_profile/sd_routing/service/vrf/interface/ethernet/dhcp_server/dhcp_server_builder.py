# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateVrfInterfaceEthernetAndDhcpServerParcelAssociationForServicePostRequest,
    CreateVrfInterfaceEthernetAndDhcpServerParcelAssociationForServicePostResponse,
    EditVrfInterfaceEthernetAndDhcpServerParcelAssociationForServicePutRequest,
    EditVrfInterfaceEthernetAndDhcpServerParcelAssociationForServicePutResponse,
    GetSingleSdRoutingServiceVrfInterfaceEthernetDhcpServerPayload,
    GetVrfInterfaceEthernetAssociatedDhcpServerParcelsForServiceGetResponse,
)


class DhcpServerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet/{ethernetId}/dhcp-server
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        service_id: str,
        vrf_id: str,
        ethernet_id: str,
        payload: CreateVrfInterfaceEthernetAndDhcpServerParcelAssociationForServicePostRequest,
        **kw,
    ) -> CreateVrfInterfaceEthernetAndDhcpServerParcelAssociationForServicePostResponse:
        """
        Associate a SD-Routing ethernet interface feature with a DHCP server feature for service feature profile
        POST /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet/{ethernetId}/dhcp-server

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param ethernet_id: Interface Feature ID
        :param payload: SD-Routing DHCP Server feature for VRF Interface in service feature profile
        :returns: CreateVrfInterfaceEthernetAndDhcpServerParcelAssociationForServicePostResponse
        """
        params = {
            "serviceId": service_id,
            "vrfId": vrf_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet/{ethernetId}/dhcp-server",
            return_type=CreateVrfInterfaceEthernetAndDhcpServerParcelAssociationForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        vrf_id: str,
        ethernet_id: str,
        dhcp_server_id: str,
        payload: EditVrfInterfaceEthernetAndDhcpServerParcelAssociationForServicePutRequest,
        **kw,
    ) -> EditVrfInterfaceEthernetAndDhcpServerParcelAssociationForServicePutResponse:
        """
        Update a SD-Routing LAN ethernet interface feature and a DHCP server feature association for service feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet/{ethernetId}/dhcp-server/{dhcpServerId}

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param ethernet_id: Interface Feature ID
        :param dhcp_server_id: DHCP Server Feature ID
        :param payload: SD-Routing DHCP Server feature for VRF Interface in service feature profile
        :returns: EditVrfInterfaceEthernetAndDhcpServerParcelAssociationForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "vrfId": vrf_id,
            "ethernetId": ethernet_id,
            "dhcpServerId": dhcp_server_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet/{ethernetId}/dhcp-server/{dhcpServerId}",
            return_type=EditVrfInterfaceEthernetAndDhcpServerParcelAssociationForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vrf_id: str, ethernet_id: str, dhcp_server_id: str, **kw):
        """
        Delete a LAN ethernet interface feature and a DHCP server feature association for service feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet/{ethernetId}/dhcp-server/{dhcpServerId}

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param ethernet_id: Interface Feature ID
        :param dhcp_server_id: DHCP Server Feature ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vrfId": vrf_id,
            "ethernetId": ethernet_id,
            "dhcpServerId": dhcp_server_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet/{ethernetId}/dhcp-server/{dhcpServerId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, vrf_id: str, ethernet_id: str, dhcp_server_id: str, **kw
    ) -> GetSingleSdRoutingServiceVrfInterfaceEthernetDhcpServerPayload:
        """
        Get the LAN ethernet interface feature associated DHCP server feature in service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet/{ethernetId}/dhcp-server/{dhcpServerId}

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param ethernet_id: Interface Feature ID
        :param dhcp_server_id: DHCP Server Feature ID
        :returns: GetSingleSdRoutingServiceVrfInterfaceEthernetDhcpServerPayload
        """
        ...

    @overload
    def get(
        self, service_id: str, vrf_id: str, ethernet_id: str, **kw
    ) -> List[GetVrfInterfaceEthernetAssociatedDhcpServerParcelsForServiceGetResponse]:
        """
        Get the ethernet interface feature associated DHCP server feature in service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet/{ethernetId}/dhcp-server

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param ethernet_id: Interface Feature ID
        :returns: List[GetVrfInterfaceEthernetAssociatedDhcpServerParcelsForServiceGetResponse]
        """
        ...

    def get(
        self,
        service_id: str,
        vrf_id: str,
        ethernet_id: str,
        dhcp_server_id: Optional[str] = None,
        **kw,
    ) -> Union[
        List[GetVrfInterfaceEthernetAssociatedDhcpServerParcelsForServiceGetResponse],
        GetSingleSdRoutingServiceVrfInterfaceEthernetDhcpServerPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet/{ethernetId}/dhcp-server/{dhcpServerId}
        if self._request_adapter.param_checker(
            [(service_id, str), (vrf_id, str), (ethernet_id, str), (dhcp_server_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vrfId": vrf_id,
                "ethernetId": ethernet_id,
                "dhcpServerId": dhcp_server_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet/{ethernetId}/dhcp-server/{dhcpServerId}",
                return_type=GetSingleSdRoutingServiceVrfInterfaceEthernetDhcpServerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet/{ethernetId}/dhcp-server
        if self._request_adapter.param_checker(
            [(service_id, str), (vrf_id, str), (ethernet_id, str)], [dhcp_server_id]
        ):
            params = {
                "serviceId": service_id,
                "vrfId": vrf_id,
                "ethernetId": ethernet_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet/{ethernetId}/dhcp-server",
                return_type=List[
                    GetVrfInterfaceEthernetAssociatedDhcpServerParcelsForServiceGetResponse
                ],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
