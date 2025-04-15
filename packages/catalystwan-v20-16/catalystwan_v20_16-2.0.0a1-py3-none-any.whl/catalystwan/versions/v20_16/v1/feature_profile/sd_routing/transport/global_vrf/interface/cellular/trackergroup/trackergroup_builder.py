# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransportPostRequest,
    CreateGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransportPostResponse,
    EditGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransportPutRequest,
    EditGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransportPutResponse,
    GetGlobalVrfInterfaceCellularAssociatedTrackerParcelsForTransportGetResponse,
    GetSingleSdRoutingTransportGlobalVrfInterfaceCellularTrackergroupPayload,
)


class TrackergroupBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/trackergroup
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        vrf_id: str,
        cellular_id: str,
        payload: CreateGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransportPostRequest,
        **kw,
    ) -> CreateGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransportPostResponse:
        """
        Associate a GlobalVRFInterfaceCellular feature with a Tracker Group Parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/trackergroup

        :param transport_id: Feature Profile ID
        :param vrf_id: Global VRF Profile ID
        :param cellular_id: Cellular Interface Profile Parcel ID
        :param payload: Tracker Profile Parcel Id
        :returns: CreateGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
            "cellularId": cellular_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/trackergroup",
            return_type=CreateGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransportPostResponse,
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
        payload: EditGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransportPutRequest,
        **kw,
    ) -> EditGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransportPutResponse:
        """
        Update a GlobalVRFInterfaceCellular feature and a Tracker Group Parcel association for transport feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/trackergroup/{trackerId}

        :param transport_id: Feature Profile ID
        :param vrf_id: Global VRF Profile ID
        :param cellular_id: Cellular Interface Profile Parcel ID
        :param tracker_id: Tracker ID
        :param payload: Tracker Profile Parcel
        :returns: EditGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
            "cellularId": cellular_id,
            "trackerId": tracker_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/trackergroup/{trackerId}",
            return_type=EditGlobalVrfInterfaceCellularAndTrackerParcelAssociationForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vrf_id: str, cellular_id: str, tracker_id: str, **kw):
        """
        Delete a GlobalVRFInterfaceCellular and a Tracker Group Feature association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/trackergroup/{trackerId}

        :param transport_id: Feature Profile ID
        :param vrf_id: Global VRF Profile ID
        :param cellular_id: Cellular Interface Profile Parcel ID
        :param tracker_id: Tracker Group Parcel ID
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
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/trackergroup/{trackerId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vrf_id: str, cellular_id: str, tracker_id: str, **kw
    ) -> GetSingleSdRoutingTransportGlobalVrfInterfaceCellularTrackergroupPayload:
        """
        Get GlobalVRFInterfaceCellular associated Tracker Group Feature by trackerId for transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/trackergroup/{trackerId}

        :param transport_id: Feature Profile ID
        :param vrf_id: Global VRF Profile ID
        :param cellular_id: Cellular Interface Profile Parcel ID
        :param tracker_id: Tracker Group Parcel ID
        :returns: GetSingleSdRoutingTransportGlobalVrfInterfaceCellularTrackergroupPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vrf_id: str, cellular_id: str, **kw
    ) -> List[GetGlobalVrfInterfaceCellularAssociatedTrackerParcelsForTransportGetResponse]:
        """
        Get GlobalVRFInterfaceCellular associated Tracker Group Features for transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/trackergroup

        :param transport_id: Feature Profile ID
        :param vrf_id: Global VRF Profile ID
        :param cellular_id: Cellular Interface Profile Parcel ID
        :returns: List[GetGlobalVrfInterfaceCellularAssociatedTrackerParcelsForTransportGetResponse]
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
        List[GetGlobalVrfInterfaceCellularAssociatedTrackerParcelsForTransportGetResponse],
        GetSingleSdRoutingTransportGlobalVrfInterfaceCellularTrackergroupPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/trackergroup/{trackerId}
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
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/trackergroup/{trackerId}",
                return_type=GetSingleSdRoutingTransportGlobalVrfInterfaceCellularTrackergroupPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/trackergroup
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
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/cellular/{cellularId}/trackergroup",
                return_type=List[
                    GetGlobalVrfInterfaceCellularAssociatedTrackerParcelsForTransportGetResponse
                ],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
