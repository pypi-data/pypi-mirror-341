# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateLanVpnAndRoutingMulticastParcelAssociationForServicePostRequest,
    CreateLanVpnAndRoutingMulticastParcelAssociationForServicePostResponse,
    EditLanVpnAndRoutingMulticastParcelAssociationForServicePutRequest,
    EditLanVpnAndRoutingMulticastParcelAssociationForServicePutResponse,
    GetLanVpnAssociatedRoutingMulticastParcelsForServiceGetResponse,
    GetSingleSdwanServiceLanVpnRoutingMulticastPayload,
)


class MulticastBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/multicast
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        service_id: str,
        vpn_id: str,
        payload: CreateLanVpnAndRoutingMulticastParcelAssociationForServicePostRequest,
        **kw,
    ) -> CreateLanVpnAndRoutingMulticastParcelAssociationForServicePostResponse:
        """
        Associate a lanvpn parcel with a routingmulticast Parcel for service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/multicast

        :param service_id: Feature Profile ID
        :param vpn_id: Lan Vpn Profile Parcel ID
        :param payload: Routing Multicast Profile Parcel Id
        :returns: CreateLanVpnAndRoutingMulticastParcelAssociationForServicePostResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/multicast",
            return_type=CreateLanVpnAndRoutingMulticastParcelAssociationForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        vpn_id: str,
        multicast_id: str,
        payload: EditLanVpnAndRoutingMulticastParcelAssociationForServicePutRequest,
        **kw,
    ) -> EditLanVpnAndRoutingMulticastParcelAssociationForServicePutResponse:
        """
        Update a LanVpn parcel and a RoutingMulticast Parcel association for service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/multicast/{multicastId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param multicast_id: Routing Multicast ID
        :param payload: Routing Multicast Profile Parcel
        :returns: EditLanVpnAndRoutingMulticastParcelAssociationForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "multicastId": multicast_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/multicast/{multicastId}",
            return_type=EditLanVpnAndRoutingMulticastParcelAssociationForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vpn_id: str, multicast_id: str, **kw):
        """
        Delete a LanVpn parcel and a RoutingMulticast Parcel association for service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/multicast/{multicastId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param multicast_id: Routing Multicast Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "multicastId": multicast_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/multicast/{multicastId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, vpn_id: str, multicast_id: str, **kw
    ) -> GetSingleSdwanServiceLanVpnRoutingMulticastPayload:
        """
        Get LanVpn parcel associated RoutingMulticast Parcel by multicastId for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/multicast/{multicastId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param multicast_id: Routing Multicast Parcel ID
        :returns: GetSingleSdwanServiceLanVpnRoutingMulticastPayload
        """
        ...

    @overload
    def get(
        self, service_id: str, vpn_id: str, **kw
    ) -> List[GetLanVpnAssociatedRoutingMulticastParcelsForServiceGetResponse]:
        """
        Get LanVpn associated Routing Multicast Parcels for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/multicast

        :param service_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :returns: List[GetLanVpnAssociatedRoutingMulticastParcelsForServiceGetResponse]
        """
        ...

    def get(
        self, service_id: str, vpn_id: str, multicast_id: Optional[str] = None, **kw
    ) -> Union[
        List[GetLanVpnAssociatedRoutingMulticastParcelsForServiceGetResponse],
        GetSingleSdwanServiceLanVpnRoutingMulticastPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/multicast/{multicastId}
        if self._request_adapter.param_checker(
            [(service_id, str), (vpn_id, str), (multicast_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
                "multicastId": multicast_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/multicast/{multicastId}",
                return_type=GetSingleSdwanServiceLanVpnRoutingMulticastPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/multicast
        if self._request_adapter.param_checker([(service_id, str), (vpn_id, str)], [multicast_id]):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/multicast",
                return_type=List[GetLanVpnAssociatedRoutingMulticastParcelsForServiceGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
