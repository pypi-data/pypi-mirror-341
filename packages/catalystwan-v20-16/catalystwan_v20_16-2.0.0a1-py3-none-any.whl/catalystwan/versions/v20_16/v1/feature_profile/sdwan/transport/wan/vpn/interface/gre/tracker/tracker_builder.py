# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateWanVpnInterfaceGreAndTrackerParcelAssociationForTransportPostRequest,
    CreateWanVpnInterfaceGreAndTrackerParcelAssociationForTransportPostResponse,
    EditWanVpnInterfaceGreAndTrackerParcelAssociationForTransportPutRequest,
    EditWanVpnInterfaceGreAndTrackerParcelAssociationForTransportPutResponse,
    GetSingleSdwanTransportWanVpnInterfaceGreTrackerPayload,
    GetWanVpnInterfaceGreAssociatedTrackerParcelsForTransportGetResponse,
)


class TrackerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre/{greId}/tracker
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        vpn_id: str,
        gre_id: str,
        payload: CreateWanVpnInterfaceGreAndTrackerParcelAssociationForTransportPostRequest,
        **kw,
    ) -> CreateWanVpnInterfaceGreAndTrackerParcelAssociationForTransportPostResponse:
        """
        Associate a WanVpnInterfaceGre parcel with a Tracker Parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre/{greId}/tracker

        :param transport_id: Feature Profile ID
        :param vpn_id: VPN Profile Parcel ID
        :param gre_id: Interface Profile Parcel ID
        :param payload: Tracker Profile Parcel Id
        :returns: CreateWanVpnInterfaceGreAndTrackerParcelAssociationForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "greId": gre_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre/{greId}/tracker",
            return_type=CreateWanVpnInterfaceGreAndTrackerParcelAssociationForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vpn_id: str,
        gre_id: str,
        tracker_id: str,
        payload: EditWanVpnInterfaceGreAndTrackerParcelAssociationForTransportPutRequest,
        **kw,
    ) -> EditWanVpnInterfaceGreAndTrackerParcelAssociationForTransportPutResponse:
        """
        Update a WanVpnInterfaceGre parcel and a Tracker Parcel association for transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre/{greId}/tracker/{trackerId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param gre_id: Interface Profile Parcel ID
        :param tracker_id: Tracker ID
        :param payload: Tracker Profile Parcel
        :returns: EditWanVpnInterfaceGreAndTrackerParcelAssociationForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "greId": gre_id,
            "trackerId": tracker_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre/{greId}/tracker/{trackerId}",
            return_type=EditWanVpnInterfaceGreAndTrackerParcelAssociationForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vpn_id: str, gre_id: str, tracker_id: str, **kw):
        """
        Delete a WanVpnInterfaceGre and a Tracker Parcel association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre/{greId}/tracker/{trackerId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param gre_id: Interface Profile Parcel ID
        :param tracker_id: Tracker Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "greId": gre_id,
            "trackerId": tracker_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre/{greId}/tracker/{trackerId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vpn_id: str, gre_id: str, tracker_id: str, **kw
    ) -> GetSingleSdwanTransportWanVpnInterfaceGreTrackerPayload:
        """
        Get WanVpnInterfaceGre associated Tracker Parcel by trackerId for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre/{greId}/tracker/{trackerId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param gre_id: Interface Profile Parcel ID
        :param tracker_id: Tracker Parcel ID
        :returns: GetSingleSdwanTransportWanVpnInterfaceGreTrackerPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vpn_id: str, gre_id: str, **kw
    ) -> List[GetWanVpnInterfaceGreAssociatedTrackerParcelsForTransportGetResponse]:
        """
        Get WanVpnInterfaceGre associated Tracker Parcels for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre/{greId}/tracker

        :param transport_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :param gre_id: Interface Profile Parcel ID
        :returns: List[GetWanVpnInterfaceGreAssociatedTrackerParcelsForTransportGetResponse]
        """
        ...

    def get(
        self, transport_id: str, vpn_id: str, gre_id: str, tracker_id: Optional[str] = None, **kw
    ) -> Union[
        List[GetWanVpnInterfaceGreAssociatedTrackerParcelsForTransportGetResponse],
        GetSingleSdwanTransportWanVpnInterfaceGreTrackerPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre/{greId}/tracker/{trackerId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (gre_id, str), (tracker_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "greId": gre_id,
                "trackerId": tracker_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre/{greId}/tracker/{trackerId}",
                return_type=GetSingleSdwanTransportWanVpnInterfaceGreTrackerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre/{greId}/tracker
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (gre_id, str)], [tracker_id]
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "greId": gre_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre/{greId}/tracker",
                return_type=List[
                    GetWanVpnInterfaceGreAssociatedTrackerParcelsForTransportGetResponse
                ],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
