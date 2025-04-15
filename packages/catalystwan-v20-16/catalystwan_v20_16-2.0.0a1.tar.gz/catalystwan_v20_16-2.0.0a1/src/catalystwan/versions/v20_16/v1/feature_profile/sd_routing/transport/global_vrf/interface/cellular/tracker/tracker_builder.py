# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransport1PostRequest,
    CreateGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransport1PostResponse,
    EditGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransport1PutRequest,
    EditGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransport1PutResponse,
    GetGlobalVrfInterfaceCellularAssociatedTrackerParcelsForTransport1GetResponse,
    GetSingleSdRoutingTransportGlobalVrfInterfaceCellularTrackerPayload,
)


class TrackerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/tracker
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        vrf_id: str,
        cellular_id: str,
        payload: CreateGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransport1PostRequest,
        **kw,
    ) -> CreateGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransport1PostResponse:
        """
        Associate a GlobalVRFInterfaceCellular parcel with a Tracker Parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/tracker

        :param transport_id: Feature Profile ID
        :param vrf_id: Global VRF Profile ID
        :param cellular_id: Cellular Interface Profile Parcel ID
        :param payload: Tracker Profile Parcel Id
        :returns: CreateGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransport1PostResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
            "cellularId": cellular_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/tracker",
            return_type=CreateGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransport1PostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vrf_id: str,
        cellular_id: str,
        tracker_id: str,
        payload: EditGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransport1PutRequest,
        **kw,
    ) -> EditGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransport1PutResponse:
        """
        Update a GlobalVRFInterfaceCellular parcel and a Tracker Parcel association for transport feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/tracker/{trackerId}

        :param transport_id: Feature Profile ID
        :param vrf_id: Global VRF Profile ID
        :param cellular_id: Cellular Interface Profile Parcel ID
        :param tracker_id: Tracker ID
        :param payload: Tracker Profile Parcel
        :returns: EditGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransport1PutResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
            "cellularId": cellular_id,
            "trackerId": tracker_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/tracker/{trackerId}",
            return_type=EditGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransport1PutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vrf_id: str, cellular_id: str, tracker_id: str, **kw):
        """
        Delete a GlobalVRFInterfaceCellular and a Tracker Parcel association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/tracker/{trackerId}

        :param transport_id: Feature Profile ID
        :param vrf_id: Global VRF Profile ID
        :param cellular_id: Cellular Interface Profile Parcel ID
        :param tracker_id: Tracker Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
            "cellularId": cellular_id,
            "trackerId": tracker_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/tracker/{trackerId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vrf_id: str, cellular_id: str, tracker_id: str, **kw
    ) -> GetSingleSdRoutingTransportGlobalVrfInterfaceCellularTrackerPayload:
        """
        Get GlobalVRFInterfaceCellular associated Tracker Parcel by trackerId for transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/tracker/{trackerId}

        :param transport_id: Feature Profile ID
        :param vrf_id: Global VRF Profile ID
        :param cellular_id: Cellular Interface Profile Parcel ID
        :param tracker_id: Tracker Parcel ID
        :returns: GetSingleSdRoutingTransportGlobalVrfInterfaceCellularTrackerPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vrf_id: str, cellular_id: str, **kw
    ) -> List[GetGlobalVrfInterfaceCellularAssociatedTrackerParcelsForTransport1GetResponse]:
        """
        Get GlobalVRFInterfaceCellular associated Tracker Parcels for transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/tracker

        :param transport_id: Feature Profile ID
        :param vrf_id: Global VRF Profile ID
        :param cellular_id: Cellular Interface Profile Parcel ID
        :returns: List[GetGlobalVrfInterfaceCellularAssociatedTrackerParcelsForTransport1GetResponse]
        """
        ...

    def get(
        self,
        transport_id: str,
        vrf_id: str,
        cellular_id: str,
        tracker_id: Optional[str] = None,
        **kw,
    ) -> Union[
        List[GetGlobalVrfInterfaceCellularAssociatedTrackerParcelsForTransport1GetResponse],
        GetSingleSdRoutingTransportGlobalVrfInterfaceCellularTrackerPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/tracker/{trackerId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vrf_id, str), (cellular_id, str), (tracker_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
                "cellularId": cellular_id,
                "trackerId": tracker_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/tracker/{trackerId}",
                return_type=GetSingleSdRoutingTransportGlobalVrfInterfaceCellularTrackerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/tracker
        if self._request_adapter.param_checker(
            [(transport_id, str), (vrf_id, str), (cellular_id, str)], [tracker_id]
        ):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
                "cellularId": cellular_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/tracker",
                return_type=List[
                    GetGlobalVrfInterfaceCellularAssociatedTrackerParcelsForTransport1GetResponse
                ],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
