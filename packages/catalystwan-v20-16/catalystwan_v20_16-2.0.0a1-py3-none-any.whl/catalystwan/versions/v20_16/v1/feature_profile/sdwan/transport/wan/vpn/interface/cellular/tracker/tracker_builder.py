# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateWanVpnInterfaceCellularAndTrackerParcelAssociationForTransportPostRequest,
    CreateWanVpnInterfaceCellularAndTrackerParcelAssociationForTransportPostResponse,
    EditWanVpnInterfaceCellularAndTrackerParcelAssociationForTransportPutRequest,
    EditWanVpnInterfaceCellularAndTrackerParcelAssociationForTransportPutResponse,
    GetSingleSdwanTransportWanVpnInterfaceCellularTrackerPayload,
    GetWanVpnInterfaceCellularAssociatedTrackerParcelsForTransportGetResponse,
)


class TrackerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/tracker
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(
        self,
        transport_id: str,
        vpn_id: str,
        cellular_id: str,
        tracker_id: str,
        payload: EditWanVpnInterfaceCellularAndTrackerParcelAssociationForTransportPutRequest,
        **kw,
    ) -> EditWanVpnInterfaceCellularAndTrackerParcelAssociationForTransportPutResponse:
        """
        Update a WanVpnInterfaceCellular parcel and a Tracker Parcel association for transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/tracker/{trackerId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param cellular_id: Interface Profile Parcel ID
        :param tracker_id: Tracker ID
        :param payload: Tracker Profile Parcel
        :returns: EditWanVpnInterfaceCellularAndTrackerParcelAssociationForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "cellularId": cellular_id,
            "trackerId": tracker_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/tracker/{trackerId}",
            return_type=EditWanVpnInterfaceCellularAndTrackerParcelAssociationForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vpn_id: str, cellular_id: str, tracker_id: str, **kw):
        """
        Delete a WanVpnInterfaceCellular and a Tracker Parcel association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/tracker/{trackerId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param cellular_id: Interface Profile Parcel ID
        :param tracker_id: Tracker Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "cellularId": cellular_id,
            "trackerId": tracker_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/tracker/{trackerId}",
            params=params,
            **kw,
        )

    def post(
        self,
        transport_id: str,
        vpn_parcel_id: str,
        cellular_id: str,
        payload: CreateWanVpnInterfaceCellularAndTrackerParcelAssociationForTransportPostRequest,
        **kw,
    ) -> CreateWanVpnInterfaceCellularAndTrackerParcelAssociationForTransportPostResponse:
        """
        Associate a WanVpnInterfaceCellular parcel with a Tracker Parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnParcelId}/interface/cellular/{cellularId}/tracker

        :param transport_id: Feature Profile ID
        :param vpn_parcel_id: VPN Profile Parcel ID
        :param cellular_id: Interface Profile Parcel ID
        :param payload: Tracker Profile Parcel Id
        :returns: CreateWanVpnInterfaceCellularAndTrackerParcelAssociationForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vpnParcelId": vpn_parcel_id,
            "cellularId": cellular_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnParcelId}/interface/cellular/{cellularId}/tracker",
            return_type=CreateWanVpnInterfaceCellularAndTrackerParcelAssociationForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vpn_id: str, cellular_id: str, tracker_id: str, **kw
    ) -> GetSingleSdwanTransportWanVpnInterfaceCellularTrackerPayload:
        """
        Get WanVpnInterfaceCellular associated Tracker Parcel by trackerId for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/tracker/{trackerId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param cellular_id: Interface Profile Parcel ID
        :param tracker_id: Tracker Parcel ID
        :returns: GetSingleSdwanTransportWanVpnInterfaceCellularTrackerPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vpn_id: str, cellular_id: str, **kw
    ) -> List[GetWanVpnInterfaceCellularAssociatedTrackerParcelsForTransportGetResponse]:
        """
        Get WanVpnInterfaceCellular associated Tracker Parcels for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/tracker

        :param transport_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :param cellular_id: Interface Profile Parcel ID
        :returns: List[GetWanVpnInterfaceCellularAssociatedTrackerParcelsForTransportGetResponse]
        """
        ...

    def get(
        self,
        transport_id: str,
        vpn_id: str,
        cellular_id: str,
        tracker_id: Optional[str] = None,
        **kw,
    ) -> Union[
        List[GetWanVpnInterfaceCellularAssociatedTrackerParcelsForTransportGetResponse],
        GetSingleSdwanTransportWanVpnInterfaceCellularTrackerPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/tracker/{trackerId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (cellular_id, str), (tracker_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "cellularId": cellular_id,
                "trackerId": tracker_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/tracker/{trackerId}",
                return_type=GetSingleSdwanTransportWanVpnInterfaceCellularTrackerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/tracker
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (cellular_id, str)], [tracker_id]
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "cellularId": cellular_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/tracker",
                return_type=List[
                    GetWanVpnInterfaceCellularAssociatedTrackerParcelsForTransportGetResponse
                ],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
