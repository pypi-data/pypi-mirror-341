# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateWanVpnInterfaceEthernetAndIpv6TrackerGroupParcelAssociationForTransportPostRequest,
    CreateWanVpnInterfaceEthernetAndIpv6TrackerGroupParcelAssociationForTransportPostResponse,
    EditWanVpnInterfaceEthernetAndIpv6TrackerGroupParcelAssociationForTransportPutRequest,
    EditWanVpnInterfaceEthernetAndIpv6TrackerGroupParcelAssociationForTransportPutResponse,
    GetSingleSdwanTransportWanVpnInterfaceEthernetIpv6TrackergroupPayload,
    GetWanVpnInterfaceEthernetAssociatedIpv6TrackerGroupParcelsForTransportGetResponse,
)


class Ipv6TrackergroupBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/ipv6-trackergroup
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(
        self,
        transport_id: str,
        vpn_id: str,
        ethernet_id: str,
        ipv6_trackergroup_id: str,
        payload: EditWanVpnInterfaceEthernetAndIpv6TrackerGroupParcelAssociationForTransportPutRequest,
        **kw,
    ) -> EditWanVpnInterfaceEthernetAndIpv6TrackerGroupParcelAssociationForTransportPutResponse:
        """
        Update a WanVpnInterfaceEthernet parcel and a IPv6 TrackerGroup Parcel association for transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/ipv6-trackergroup/{ipv6-trackergroupId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param ipv6_trackergroup_id: TrackerGroup ID
        :param payload: IPv6 TrackerGroup Profile Parcel
        :returns: EditWanVpnInterfaceEthernetAndIpv6TrackerGroupParcelAssociationForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "ethernetId": ethernet_id,
            "ipv6-trackergroupId": ipv6_trackergroup_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/ipv6-trackergroup/{ipv6-trackergroupId}",
            return_type=EditWanVpnInterfaceEthernetAndIpv6TrackerGroupParcelAssociationForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(
        self, transport_id: str, vpn_id: str, ethernet_id: str, ipv6_trackergroup_id: str, **kw
    ):
        """
        Delete a WanVpnInterfaceEthernet and a IPv6 TrackerGroup Parcel association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/ipv6-trackergroup/{ipv6-trackergroupId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param ipv6_trackergroup_id: TrackerGroup Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "ethernetId": ethernet_id,
            "ipv6-trackergroupId": ipv6_trackergroup_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/ipv6-trackergroup/{ipv6-trackergroupId}",
            params=params,
            **kw,
        )

    def post(
        self,
        transport_id: str,
        vpn_parcel_id: str,
        ethernet_id: str,
        payload: CreateWanVpnInterfaceEthernetAndIpv6TrackerGroupParcelAssociationForTransportPostRequest,
        **kw,
    ) -> CreateWanVpnInterfaceEthernetAndIpv6TrackerGroupParcelAssociationForTransportPostResponse:
        """
        Associate a WanVpnInterfaceEthernet parcel with a IPv6 TrackerGroup Parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnParcelId}/interface/ethernet/{ethernetId}/ipv6-trackergroup

        :param transport_id: Feature Profile ID
        :param vpn_parcel_id: VPN Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param payload: IPv6 TrackerGroup Profile Parcel Id
        :returns: CreateWanVpnInterfaceEthernetAndIpv6TrackerGroupParcelAssociationForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vpnParcelId": vpn_parcel_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnParcelId}/interface/ethernet/{ethernetId}/ipv6-trackergroup",
            return_type=CreateWanVpnInterfaceEthernetAndIpv6TrackerGroupParcelAssociationForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vpn_id: str, ethernet_id: str, ipv6_trackergroup_id: str, **kw
    ) -> GetSingleSdwanTransportWanVpnInterfaceEthernetIpv6TrackergroupPayload:
        """
        Get WanVpnInterfaceEthernet associated IPv6 TrackerGroup Parcel by ipv6-trackergroupId for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/ipv6-trackergroup/{ipv6-trackergroupId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param ipv6_trackergroup_id: TrackerGroup Parcel ID
        :returns: GetSingleSdwanTransportWanVpnInterfaceEthernetIpv6TrackergroupPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vpn_id: str, ethernet_id: str, **kw
    ) -> List[GetWanVpnInterfaceEthernetAssociatedIpv6TrackerGroupParcelsForTransportGetResponse]:
        """
        Get WanVpnInterfaceEthernet associated IPv6 TrackerGroup Parcels for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/ipv6-trackergroup

        :param transport_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :returns: List[GetWanVpnInterfaceEthernetAssociatedIpv6TrackerGroupParcelsForTransportGetResponse]
        """
        ...

    def get(
        self,
        transport_id: str,
        vpn_id: str,
        ethernet_id: str,
        ipv6_trackergroup_id: Optional[str] = None,
        **kw,
    ) -> Union[
        List[GetWanVpnInterfaceEthernetAssociatedIpv6TrackerGroupParcelsForTransportGetResponse],
        GetSingleSdwanTransportWanVpnInterfaceEthernetIpv6TrackergroupPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/ipv6-trackergroup/{ipv6-trackergroupId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (ethernet_id, str), (ipv6_trackergroup_id, str)],
            [],
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "ethernetId": ethernet_id,
                "ipv6-trackergroupId": ipv6_trackergroup_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/ipv6-trackergroup/{ipv6-trackergroupId}",
                return_type=GetSingleSdwanTransportWanVpnInterfaceEthernetIpv6TrackergroupPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/ipv6-trackergroup
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (ethernet_id, str)], [ipv6_trackergroup_id]
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "ethernetId": ethernet_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/ipv6-trackergroup",
                return_type=List[
                    GetWanVpnInterfaceEthernetAssociatedIpv6TrackerGroupParcelsForTransportGetResponse
                ],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
