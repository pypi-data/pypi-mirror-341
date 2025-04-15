# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateWanVpnInterfaceIpsecAndTrackerParcelAssociationForTransportPostRequest,
    CreateWanVpnInterfaceIpsecAndTrackerParcelAssociationForTransportPostResponse,
    EditWanVpnInterfaceIpsecAndTrackerParcelAssociationForTransportPutRequest,
    EditWanVpnInterfaceIpsecAndTrackerParcelAssociationForTransportPutResponse,
    GetSingleSdwanTransportWanVpnInterfaceIpsecTrackerPayload,
    GetWanVpnInterfaceIpsecAssociatedTrackerParcelsForTransportGetResponse,
)


class TrackerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec/{ipsecId}/tracker
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(
        self,
        transport_id: str,
        vpn_id: str,
        ipsec_id: str,
        tracker_id: str,
        payload: EditWanVpnInterfaceIpsecAndTrackerParcelAssociationForTransportPutRequest,
        **kw,
    ) -> EditWanVpnInterfaceIpsecAndTrackerParcelAssociationForTransportPutResponse:
        """
        Update a WanVpnInterfaceIpsec parcel and a Tracker Parcel association for transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec/{ipsecId}/tracker/{trackerId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ipsec_id: Interface Profile Parcel ID
        :param tracker_id: Tracker ID
        :param payload: Tracker Profile Parcel
        :returns: EditWanVpnInterfaceIpsecAndTrackerParcelAssociationForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "ipsecId": ipsec_id,
            "trackerId": tracker_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec/{ipsecId}/tracker/{trackerId}",
            return_type=EditWanVpnInterfaceIpsecAndTrackerParcelAssociationForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vpn_id: str, ipsec_id: str, tracker_id: str, **kw):
        """
        Delete a WanVpnInterfaceIpsec and a Tracker Parcel association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec/{ipsecId}/tracker/{trackerId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ipsec_id: Interface Profile Parcel ID
        :param tracker_id: Tracker Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "ipsecId": ipsec_id,
            "trackerId": tracker_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec/{ipsecId}/tracker/{trackerId}",
            params=params,
            **kw,
        )

    def post(
        self,
        transport_id: str,
        vpn_parcel_id: str,
        ipsec_id: str,
        payload: CreateWanVpnInterfaceIpsecAndTrackerParcelAssociationForTransportPostRequest,
        **kw,
    ) -> CreateWanVpnInterfaceIpsecAndTrackerParcelAssociationForTransportPostResponse:
        """
        Associate a WanVpnInterfaceIpsec parcel with a Tracker Parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnParcelId}/interface/ipsec/{ipsecId}/tracker

        :param transport_id: Feature Profile ID
        :param vpn_parcel_id: VPN Profile Parcel ID
        :param ipsec_id: Interface Profile Parcel ID
        :param payload: Tracker Profile Parcel Id
        :returns: CreateWanVpnInterfaceIpsecAndTrackerParcelAssociationForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vpnParcelId": vpn_parcel_id,
            "ipsecId": ipsec_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnParcelId}/interface/ipsec/{ipsecId}/tracker",
            return_type=CreateWanVpnInterfaceIpsecAndTrackerParcelAssociationForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vpn_id: str, ipsec_id: str, tracker_id: str, **kw
    ) -> GetSingleSdwanTransportWanVpnInterfaceIpsecTrackerPayload:
        """
        Get WanVpnInterfaceIpsec associated Tracker Parcel by trackerId for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec/{ipsecId}/tracker/{trackerId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ipsec_id: Interface Profile Parcel ID
        :param tracker_id: Tracker Parcel ID
        :returns: GetSingleSdwanTransportWanVpnInterfaceIpsecTrackerPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vpn_id: str, ipsec_id: str, **kw
    ) -> List[GetWanVpnInterfaceIpsecAssociatedTrackerParcelsForTransportGetResponse]:
        """
        Get WanVpnInterfaceIpsec associated Tracker Parcels for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec/{ipsecId}/tracker

        :param transport_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :param ipsec_id: Interface Profile Parcel ID
        :returns: List[GetWanVpnInterfaceIpsecAssociatedTrackerParcelsForTransportGetResponse]
        """
        ...

    def get(
        self, transport_id: str, vpn_id: str, ipsec_id: str, tracker_id: Optional[str] = None, **kw
    ) -> Union[
        List[GetWanVpnInterfaceIpsecAssociatedTrackerParcelsForTransportGetResponse],
        GetSingleSdwanTransportWanVpnInterfaceIpsecTrackerPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec/{ipsecId}/tracker/{trackerId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (ipsec_id, str), (tracker_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "ipsecId": ipsec_id,
                "trackerId": tracker_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec/{ipsecId}/tracker/{trackerId}",
                return_type=GetSingleSdwanTransportWanVpnInterfaceIpsecTrackerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec/{ipsecId}/tracker
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (ipsec_id, str)], [tracker_id]
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "ipsecId": ipsec_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ipsec/{ipsecId}/tracker",
                return_type=List[
                    GetWanVpnInterfaceIpsecAssociatedTrackerParcelsForTransportGetResponse
                ],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
