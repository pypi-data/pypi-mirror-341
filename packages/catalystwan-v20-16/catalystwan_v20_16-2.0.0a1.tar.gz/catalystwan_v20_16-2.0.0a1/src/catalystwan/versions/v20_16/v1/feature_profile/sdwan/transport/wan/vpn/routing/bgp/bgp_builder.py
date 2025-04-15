# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateWanVpnAndRoutingBgpParcelAssociationForTransportPostRequest,
    CreateWanVpnAndRoutingBgpParcelAssociationForTransportPostResponse,
    EditWanVpnAndRoutingBgpParcelAssociationForTransportPutRequest,
    EditWanVpnAndRoutingBgpParcelAssociationForTransportPutResponse,
    GetSingleSdwanTransportWanVpnRoutingBgpPayload,
    GetWanVpnAssociatedRoutingBgpParcelsForTransportGetResponse,
)


class BgpBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/bgp
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        vpn_id: str,
        payload: CreateWanVpnAndRoutingBgpParcelAssociationForTransportPostRequest,
        **kw,
    ) -> CreateWanVpnAndRoutingBgpParcelAssociationForTransportPostResponse:
        """
        Associate a wanvpn parcel with a routingbgp Parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/bgp

        :param transport_id: Feature Profile ID
        :param vpn_id: Wan Vpn Profile Parcel ID
        :param payload: Routing Bgp Profile Parcel Id
        :returns: CreateWanVpnAndRoutingBgpParcelAssociationForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/bgp",
            return_type=CreateWanVpnAndRoutingBgpParcelAssociationForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vpn_id: str,
        bgp_id: str,
        payload: EditWanVpnAndRoutingBgpParcelAssociationForTransportPutRequest,
        **kw,
    ) -> EditWanVpnAndRoutingBgpParcelAssociationForTransportPutResponse:
        """
        Update a WanVpn parcel and a RoutingBgp Parcel association for transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/bgp/{bgpId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param bgp_id: Routing Bgp ID
        :param payload: Routing Bgp Profile Parcel
        :returns: EditWanVpnAndRoutingBgpParcelAssociationForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "bgpId": bgp_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/bgp/{bgpId}",
            return_type=EditWanVpnAndRoutingBgpParcelAssociationForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vpn_id: str, bgp_id: str, **kw):
        """
        Delete a WanVpn parcel and a RoutingBgp Parcel association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/bgp/{bgpId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param bgp_id: Routing Bgp Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "bgpId": bgp_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/bgp/{bgpId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vpn_id: str, bgp_id: str, **kw
    ) -> GetSingleSdwanTransportWanVpnRoutingBgpPayload:
        """
        Get WanVpn parcel associated RoutingBgp Parcel by bgpId for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/bgp/{bgpId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param bgp_id: Routing Bgp Parcel ID
        :returns: GetSingleSdwanTransportWanVpnRoutingBgpPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vpn_id: str, **kw
    ) -> List[GetWanVpnAssociatedRoutingBgpParcelsForTransportGetResponse]:
        """
        Get WanVpn associated Routing Bgp Parcels for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/bgp

        :param transport_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :returns: List[GetWanVpnAssociatedRoutingBgpParcelsForTransportGetResponse]
        """
        ...

    def get(
        self, transport_id: str, vpn_id: str, bgp_id: Optional[str] = None, **kw
    ) -> Union[
        List[GetWanVpnAssociatedRoutingBgpParcelsForTransportGetResponse],
        GetSingleSdwanTransportWanVpnRoutingBgpPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/bgp/{bgpId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (bgp_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "bgpId": bgp_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/bgp/{bgpId}",
                return_type=GetSingleSdwanTransportWanVpnRoutingBgpPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/bgp
        if self._request_adapter.param_checker([(transport_id, str), (vpn_id, str)], [bgp_id]):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/bgp",
                return_type=List[GetWanVpnAssociatedRoutingBgpParcelsForTransportGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
