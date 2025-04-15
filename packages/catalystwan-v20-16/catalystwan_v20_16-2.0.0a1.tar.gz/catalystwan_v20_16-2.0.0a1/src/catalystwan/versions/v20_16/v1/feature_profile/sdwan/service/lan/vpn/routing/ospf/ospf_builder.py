# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateLanVpnAndRoutingOspfParcelAssociationForServicePostRequest,
    CreateLanVpnAndRoutingOspfParcelAssociationForServicePostResponse,
    EditLanVpnAndRoutingOspfParcelAssociationForServicePutRequest,
    EditLanVpnAndRoutingOspfParcelAssociationForServicePutResponse,
    GetLanVpnAssociatedRoutingOspfParcelsForServiceGetResponse,
    GetSingleSdwanServiceLanVpnRoutingOspfPayload,
)


class OspfBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospf
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        service_id: str,
        vpn_id: str,
        payload: CreateLanVpnAndRoutingOspfParcelAssociationForServicePostRequest,
        **kw,
    ) -> CreateLanVpnAndRoutingOspfParcelAssociationForServicePostResponse:
        """
        Associate a lanvpn parcel with a routingospf Parcel for service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospf

        :param service_id: Feature Profile ID
        :param vpn_id: Lan Vpn Profile Parcel ID
        :param payload: Routing Ospf Profile Parcel Id
        :returns: CreateLanVpnAndRoutingOspfParcelAssociationForServicePostResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospf",
            return_type=CreateLanVpnAndRoutingOspfParcelAssociationForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        vpn_id: str,
        ospf_id: str,
        payload: EditLanVpnAndRoutingOspfParcelAssociationForServicePutRequest,
        **kw,
    ) -> EditLanVpnAndRoutingOspfParcelAssociationForServicePutResponse:
        """
        Update a LanVpn parcel and a RoutingOspf Parcel association for service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospf/{ospfId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ospf_id: Routing Ospf ID
        :param payload: Routing Ospf Profile Parcel
        :returns: EditLanVpnAndRoutingOspfParcelAssociationForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "ospfId": ospf_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospf/{ospfId}",
            return_type=EditLanVpnAndRoutingOspfParcelAssociationForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vpn_id: str, ospf_id: str, **kw):
        """
        Delete a LanVpn parcel and a RoutingOspf Parcel association for service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospf/{ospfId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ospf_id: Routing Ospf Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "ospfId": ospf_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospf/{ospfId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, vpn_id: str, ospf_id: str, **kw
    ) -> GetSingleSdwanServiceLanVpnRoutingOspfPayload:
        """
        Get LanVpn parcel associated RoutingOspf Parcel by ospfId for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospf/{ospfId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ospf_id: Routing Ospf Parcel ID
        :returns: GetSingleSdwanServiceLanVpnRoutingOspfPayload
        """
        ...

    @overload
    def get(
        self, service_id: str, vpn_id: str, **kw
    ) -> List[GetLanVpnAssociatedRoutingOspfParcelsForServiceGetResponse]:
        """
        Get LanVpn associated Routing Ospf Parcels for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospf

        :param service_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :returns: List[GetLanVpnAssociatedRoutingOspfParcelsForServiceGetResponse]
        """
        ...

    def get(
        self, service_id: str, vpn_id: str, ospf_id: Optional[str] = None, **kw
    ) -> Union[
        List[GetLanVpnAssociatedRoutingOspfParcelsForServiceGetResponse],
        GetSingleSdwanServiceLanVpnRoutingOspfPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospf/{ospfId}
        if self._request_adapter.param_checker(
            [(service_id, str), (vpn_id, str), (ospf_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
                "ospfId": ospf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospf/{ospfId}",
                return_type=GetSingleSdwanServiceLanVpnRoutingOspfPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospf
        if self._request_adapter.param_checker([(service_id, str), (vpn_id, str)], [ospf_id]):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospf",
                return_type=List[GetLanVpnAssociatedRoutingOspfParcelsForServiceGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
