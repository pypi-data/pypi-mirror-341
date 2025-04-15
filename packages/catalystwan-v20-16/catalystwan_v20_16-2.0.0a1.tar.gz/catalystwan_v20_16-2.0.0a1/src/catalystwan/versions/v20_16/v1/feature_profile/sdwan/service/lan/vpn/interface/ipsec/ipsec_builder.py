# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateIpSecProfileParcelPostRequest,
    CreateIpSecProfileParcelPostResponse,
    EditProfileParcelPutRequest,
    EditProfileParcelPutResponse,
    GetListSdwanServiceLanVpnInterfaceIpsecPayload,
    GetSingleSdwanServiceLanVpnInterfaceIpsecPayload,
)

if TYPE_CHECKING:
    from .dhcp_server.dhcp_server_builder import DhcpServerBuilder
    from .schema.schema_builder import SchemaBuilder


class IpsecBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/lan/vpn/interface/ipsec
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, service_id: str, vpn_id: str, payload: CreateIpSecProfileParcelPostRequest, **kw
    ) -> CreateIpSecProfileParcelPostResponse:
        """
        Create a LanVpn InterfaceIpsec parcel for service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param payload: Wan Vpn Interface Ipsec Profile Parcel
        :returns: CreateIpSecProfileParcelPostResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec",
            return_type=CreateIpSecProfileParcelPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        vpn_id: str,
        ipsec_id: str,
        payload: EditProfileParcelPutRequest,
        **kw,
    ) -> EditProfileParcelPutResponse:
        """
        Update a LanVpn Interface Ipsec Parcel for Service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec/{ipsecId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ipsec_id: Interface ID
        :param payload: Lan Vpn Interface Ipsec Profile Parcel
        :returns: EditProfileParcelPutResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "ipsecId": ipsec_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec/{ipsecId}",
            return_type=EditProfileParcelPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vpn_id: str, ipsec_id: str, **kw):
        """
        Delete a  LanVpn InterfaceIpsec Parcel for Service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec/{ipsecId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ipsec_id: Interface Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "ipsecId": ipsec_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec/{ipsecId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, vpn_id: str, ipsec_id: str, **kw
    ) -> GetSingleSdwanServiceLanVpnInterfaceIpsecPayload:
        """
        Get LanVpn InterfaceIpsec Parcel by ethernetId for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec/{ipsecId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ipsec_id: Interface Parcel ID
        :returns: GetSingleSdwanServiceLanVpnInterfaceIpsecPayload
        """
        ...

    @overload
    def get(
        self, service_id: str, vpn_id: str, **kw
    ) -> GetListSdwanServiceLanVpnInterfaceIpsecPayload:
        """
        Get InterfaceIpsec Parcels for Service LanVpn Parcel
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec

        :param service_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :returns: GetListSdwanServiceLanVpnInterfaceIpsecPayload
        """
        ...

    def get(
        self, service_id: str, vpn_id: str, ipsec_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanServiceLanVpnInterfaceIpsecPayload,
        GetSingleSdwanServiceLanVpnInterfaceIpsecPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec/{ipsecId}
        if self._request_adapter.param_checker(
            [(service_id, str), (vpn_id, str), (ipsec_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
                "ipsecId": ipsec_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec/{ipsecId}",
                return_type=GetSingleSdwanServiceLanVpnInterfaceIpsecPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec
        if self._request_adapter.param_checker([(service_id, str), (vpn_id, str)], [ipsec_id]):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ipsec",
                return_type=GetListSdwanServiceLanVpnInterfaceIpsecPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def dhcp_server(self) -> DhcpServerBuilder:
        """
        The dhcp-server property
        """
        from .dhcp_server.dhcp_server_builder import DhcpServerBuilder

        return DhcpServerBuilder(self._request_adapter)

    @property
    def schema(self) -> SchemaBuilder:
        """
        The schema property
        """
        from .schema.schema_builder import SchemaBuilder

        return SchemaBuilder(self._request_adapter)
