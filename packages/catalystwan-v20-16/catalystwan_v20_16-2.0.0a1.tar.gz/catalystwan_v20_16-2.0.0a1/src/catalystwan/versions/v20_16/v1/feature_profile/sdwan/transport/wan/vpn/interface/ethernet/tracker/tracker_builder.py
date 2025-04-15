# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateWanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPostRequest,
    CreateWanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPostResponse,
    EditWanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPutRequest,
    EditWanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPutResponse,
    GetSingleSdwanTransportWanVpnInterfaceEthernetTrackerPayload,
    GetWanVpnInterfaceEthernetAssociatedTrackerParcelsForTransportGetResponse,
)


class TrackerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(
        self,
        transport_id: str,
        vpn_id: str,
        ethernet_id: str,
        tracker_id: str,
        payload: EditWanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPutRequest,
        **kw,
    ) -> EditWanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPutResponse:
        """
        Update a WanVpnInterfaceEthernet parcel and a Tracker Parcel association for transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker/{trackerId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param tracker_id: Tracker ID
        :param payload: Tracker Profile Parcel
        :returns: EditWanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "ethernetId": ethernet_id,
            "trackerId": tracker_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker/{trackerId}",
            return_type=EditWanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vpn_id: str, ethernet_id: str, tracker_id: str, **kw):
        """
        Delete a WanVpnInterfaceEthernet and a Tracker Parcel association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker/{trackerId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param tracker_id: Tracker Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "ethernetId": ethernet_id,
            "trackerId": tracker_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker/{trackerId}",
            params=params,
            **kw,
        )

    def post(
        self,
        transport_id: str,
        vpn_parcel_id: str,
        ethernet_id: str,
        payload: CreateWanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPostRequest,
        **kw,
    ) -> CreateWanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPostResponse:
        """
        Associate a WanVpnInterfaceEthernet parcel with a Tracker Parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnParcelId}/interface/ethernet/{ethernetId}/tracker

        :param transport_id: Feature Profile ID
        :param vpn_parcel_id: VPN Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param payload: Tracker Profile Parcel Id
        :returns: CreateWanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vpnParcelId": vpn_parcel_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnParcelId}/interface/ethernet/{ethernetId}/tracker",
            return_type=CreateWanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vpn_id: str, ethernet_id: str, tracker_id: str, **kw
    ) -> GetSingleSdwanTransportWanVpnInterfaceEthernetTrackerPayload:
        """
        Get WanVpnInterfaceEthernet associated Tracker Parcel by trackerId for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker/{trackerId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param tracker_id: Tracker Parcel ID
        :returns: GetSingleSdwanTransportWanVpnInterfaceEthernetTrackerPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vpn_id: str, ethernet_id: str, **kw
    ) -> List[GetWanVpnInterfaceEthernetAssociatedTrackerParcelsForTransportGetResponse]:
        """
        Get WanVpnInterfaceEthernet associated Tracker Parcels for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker

        :param transport_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :returns: List[GetWanVpnInterfaceEthernetAssociatedTrackerParcelsForTransportGetResponse]
        """
        ...

    def get(
        self,
        transport_id: str,
        vpn_id: str,
        ethernet_id: str,
        tracker_id: Optional[str] = None,
        **kw,
    ) -> Union[
        List[GetWanVpnInterfaceEthernetAssociatedTrackerParcelsForTransportGetResponse],
        GetSingleSdwanTransportWanVpnInterfaceEthernetTrackerPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker/{trackerId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (ethernet_id, str), (tracker_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "ethernetId": ethernet_id,
                "trackerId": tracker_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker/{trackerId}",
                return_type=GetSingleSdwanTransportWanVpnInterfaceEthernetTrackerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (ethernet_id, str)], [tracker_id]
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "ethernetId": ethernet_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}/tracker",
                return_type=List[
                    GetWanVpnInterfaceEthernetAssociatedTrackerParcelsForTransportGetResponse
                ],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
