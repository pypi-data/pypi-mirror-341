# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateLanVpnAndRoutingOspfv3IPv6ParcelAssociationForServicePostRequest,
    CreateLanVpnAndRoutingOspfv3IPv6ParcelAssociationForServicePostResponse,
    EditLanVpnAndRoutingOspfv3IPv6ParcelAssociationForServicePutRequest,
    EditLanVpnAndRoutingOspfv3IPv6ParcelAssociationForServicePutResponse,
    GetLanVpnAssociatedRoutingOspfv3IPv6ParcelsForServiceGetResponse,
    GetSingleSdwanServiceLanVpnRoutingOspfv3Ipv6Payload,
)


class Ipv6Builder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv6
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        service_id: str,
        vpn_id: str,
        payload: CreateLanVpnAndRoutingOspfv3IPv6ParcelAssociationForServicePostRequest,
        **kw,
    ) -> CreateLanVpnAndRoutingOspfv3IPv6ParcelAssociationForServicePostResponse:
        """
        Associate a LAN VPN parcel with a IPv6 address family OSPFv3 Parcel for service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv6

        :param service_id: Feature Profile ID
        :param vpn_id: Lan Vpn Profile Parcel ID
        :param payload: IPv6 address family OSPFv3 Profile Parcel Id
        :returns: CreateLanVpnAndRoutingOspfv3IPv6ParcelAssociationForServicePostResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv6",
            return_type=CreateLanVpnAndRoutingOspfv3IPv6ParcelAssociationForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        vpn_id: str,
        ospfv3_id: str,
        payload: EditLanVpnAndRoutingOspfv3IPv6ParcelAssociationForServicePutRequest,
        **kw,
    ) -> EditLanVpnAndRoutingOspfv3IPv6ParcelAssociationForServicePutResponse:
        """
        Update a LAN VPN parcel and a routing OSPFv3 IPv6 Parcel association for service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv6/{ospfv3Id}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ospfv3_id: IPv6 address family OSPFv3 ID
        :param payload: IPv6 address family OSPFv3 Profile Parcel
        :returns: EditLanVpnAndRoutingOspfv3IPv6ParcelAssociationForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv6/{ospfv3Id}",
            return_type=EditLanVpnAndRoutingOspfv3IPv6ParcelAssociationForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vpn_id: str, ospfv3_id: str, **kw):
        """
        Delete a LAN VPN parcel and a IPv6 OSPFv3 parcel association for service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv6/{ospfv3Id}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ospfv3_id: IPv6 Address Family OSPFv3 IPv6 Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv6/{ospfv3Id}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, vpn_id: str, ospfv3_id: str, **kw
    ) -> GetSingleSdwanServiceLanVpnRoutingOspfv3Ipv6Payload:
        """
        Get LanVpn parcel associated IPv6 address family OSPFv3 IPv6 Parcel by ospfv3Id for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv6/{ospfv3Id}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ospfv3_id: IPv6 Address Family OSPFv3 Parcel ID
        :returns: GetSingleSdwanServiceLanVpnRoutingOspfv3Ipv6Payload
        """
        ...

    @overload
    def get(
        self, service_id: str, vpn_id: str, **kw
    ) -> List[GetLanVpnAssociatedRoutingOspfv3IPv6ParcelsForServiceGetResponse]:
        """
        Get LanVpn associated IPv6 address family OSPFv3 Parcels for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv6

        :param service_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :returns: List[GetLanVpnAssociatedRoutingOspfv3IPv6ParcelsForServiceGetResponse]
        """
        ...

    def get(
        self, service_id: str, vpn_id: str, ospfv3_id: Optional[str] = None, **kw
    ) -> Union[
        List[GetLanVpnAssociatedRoutingOspfv3IPv6ParcelsForServiceGetResponse],
        GetSingleSdwanServiceLanVpnRoutingOspfv3Ipv6Payload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv6/{ospfv3Id}
        if self._request_adapter.param_checker(
            [(service_id, str), (vpn_id, str), (ospfv3_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
                "ospfv3Id": ospfv3_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv6/{ospfv3Id}",
                return_type=GetSingleSdwanServiceLanVpnRoutingOspfv3Ipv6Payload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv6
        if self._request_adapter.param_checker([(service_id, str), (vpn_id, str)], [ospfv3_id]):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv6",
                return_type=List[GetLanVpnAssociatedRoutingOspfv3IPv6ParcelsForServiceGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
