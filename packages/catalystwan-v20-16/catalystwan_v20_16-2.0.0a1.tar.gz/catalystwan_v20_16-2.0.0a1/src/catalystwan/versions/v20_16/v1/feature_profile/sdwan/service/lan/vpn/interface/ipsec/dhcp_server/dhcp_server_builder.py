# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateLanVpnInterfaceIpsecAndDhcpServerParcelAssociationForTransportPostRequest,
    CreateLanVpnInterfaceIpsecAndDhcpServerParcelAssociationForTransportPostResponse,
    EditLanVpnInterfaceIpsecAndDhcpServerParcelAssociationForTransportPutRequest,
    EditLanVpnInterfaceIpsecAndDhcpServerParcelAssociationForTransportPutResponse,
    GetLanVpnInterfaceIpsecAssociatedDhcpServerParcelsForTransportGetResponse,
    GetSingleSdwanServiceLanVpnInterfaceIpsecDhcpServerPayload,
)


class DhcpServerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec/{ipsecId}/dhcp-server
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(
        self,
        service_id: str,
        vpn_id: str,
        ipsec_id: str,
        dhcp_server_id: str,
        payload: EditLanVpnInterfaceIpsecAndDhcpServerParcelAssociationForTransportPutRequest,
        **kw,
    ) -> EditLanVpnInterfaceIpsecAndDhcpServerParcelAssociationForTransportPutResponse:
        """
        Update a LanVpnInterfaceIpsec parcel and a DhcpServer Parcel association for service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec/{ipsecId}/dhcp-server/{dhcpServerId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ipsec_id: Interface Profile Parcel ID
        :param dhcp_server_id: DhcpServer ID
        :param payload: DhcpServer Profile Parcel
        :returns: EditLanVpnInterfaceIpsecAndDhcpServerParcelAssociationForTransportPutResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "ipsecId": ipsec_id,
            "dhcpServerId": dhcp_server_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec/{ipsecId}/dhcp-server/{dhcpServerId}",
            return_type=EditLanVpnInterfaceIpsecAndDhcpServerParcelAssociationForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vpn_id: str, ipsec_id: str, dhcp_server_id: str, **kw):
        """
        Delete a LanVpnInterfaceIpsec and a DhcpServer Parcel association for service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec/{ipsecId}/dhcp-server/{dhcpServerId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ipsec_id: Interface Profile Parcel ID
        :param dhcp_server_id: DhcpServer Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "ipsecId": ipsec_id,
            "dhcpServerId": dhcp_server_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec/{ipsecId}/dhcp-server/{dhcpServerId}",
            params=params,
            **kw,
        )

    def post(
        self,
        service_id: str,
        vpn_parcel_id: str,
        ipsec_id: str,
        payload: CreateLanVpnInterfaceIpsecAndDhcpServerParcelAssociationForTransportPostRequest,
        **kw,
    ) -> CreateLanVpnInterfaceIpsecAndDhcpServerParcelAssociationForTransportPostResponse:
        """
        Associate a LanVpnInterfaceIpsec parcel with a DhcpServer Parcel for service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnParcelId}/interface/ipsec/{ipsecId}/dhcp-server

        :param service_id: Feature Profile ID
        :param vpn_parcel_id: VPN Profile Parcel ID
        :param ipsec_id: Interface Profile Parcel ID
        :param payload: DhcpServer Profile Parcel Id
        :returns: CreateLanVpnInterfaceIpsecAndDhcpServerParcelAssociationForTransportPostResponse
        """
        params = {
            "serviceId": service_id,
            "vpnParcelId": vpn_parcel_id,
            "ipsecId": ipsec_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnParcelId}/interface/ipsec/{ipsecId}/dhcp-server",
            return_type=CreateLanVpnInterfaceIpsecAndDhcpServerParcelAssociationForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, vpn_id: str, ipsec_id: str, dhcp_server_id: str, **kw
    ) -> GetSingleSdwanServiceLanVpnInterfaceIpsecDhcpServerPayload:
        """
        Get LanVpnInterfaceIpsec associated DhcpServer Parcel by dhcpServerId for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec/{ipsecId}/dhcp-server/{dhcpServerId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ipsec_id: Interface Profile Parcel ID
        :param dhcp_server_id: DhcpServer Parcel ID
        :returns: GetSingleSdwanServiceLanVpnInterfaceIpsecDhcpServerPayload
        """
        ...

    @overload
    def get(
        self, service_id: str, vpn_id: str, ipsec_id: str, **kw
    ) -> List[GetLanVpnInterfaceIpsecAssociatedDhcpServerParcelsForTransportGetResponse]:
        """
        Get LanVpnInterfaceIpsec associated DhcpServer Parcels for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec/{ipsecId}/dhcp-server

        :param service_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :param ipsec_id: Interface Profile Parcel ID
        :returns: List[GetLanVpnInterfaceIpsecAssociatedDhcpServerParcelsForTransportGetResponse]
        """
        ...

    def get(
        self,
        service_id: str,
        vpn_id: str,
        ipsec_id: str,
        dhcp_server_id: Optional[str] = None,
        **kw,
    ) -> Union[
        List[GetLanVpnInterfaceIpsecAssociatedDhcpServerParcelsForTransportGetResponse],
        GetSingleSdwanServiceLanVpnInterfaceIpsecDhcpServerPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec/{ipsecId}/dhcp-server/{dhcpServerId}
        if self._request_adapter.param_checker(
            [(service_id, str), (vpn_id, str), (ipsec_id, str), (dhcp_server_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
                "ipsecId": ipsec_id,
                "dhcpServerId": dhcp_server_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec/{ipsecId}/dhcp-server/{dhcpServerId}",
                return_type=GetSingleSdwanServiceLanVpnInterfaceIpsecDhcpServerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec/{ipsecId}/dhcp-server
        if self._request_adapter.param_checker(
            [(service_id, str), (vpn_id, str), (ipsec_id, str)], [dhcp_server_id]
        ):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
                "ipsecId": ipsec_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec/{ipsecId}/dhcp-server",
                return_type=List[
                    GetLanVpnInterfaceIpsecAssociatedDhcpServerParcelsForTransportGetResponse
                ],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
