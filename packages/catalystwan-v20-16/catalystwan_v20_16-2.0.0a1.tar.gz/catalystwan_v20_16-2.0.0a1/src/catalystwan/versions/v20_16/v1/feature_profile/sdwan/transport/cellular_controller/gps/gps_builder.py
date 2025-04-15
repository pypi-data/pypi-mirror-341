# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateCellularControllerAndGpsParcelAssociationForTransportPostRequest,
    CreateCellularControllerAndGpsParcelAssociationForTransportPostResponse,
    EditCellularControllerAndGpsParcelAssociationForTransportPutRequest,
    EditCellularControllerAndGpsParcelAssociationForTransportPutResponse,
    GetCellularControllerAssociatedGpsParcelsForTransportGetResponse,
    GetSingleSdwanTransportCellularControllerGpsPayload,
)


class GpsBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/gps
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        cellular_controller_id: str,
        payload: CreateCellularControllerAndGpsParcelAssociationForTransportPostRequest,
        **kw,
    ) -> CreateCellularControllerAndGpsParcelAssociationForTransportPostResponse:
        """
        Associate a cellularcontroller parcel with a gps Parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/gps

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Cellular Controller Profile Parcel ID
        :param payload: Gps Profile Parcel Id
        :returns: CreateCellularControllerAndGpsParcelAssociationForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "cellularControllerId": cellular_controller_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/gps",
            return_type=CreateCellularControllerAndGpsParcelAssociationForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        cellular_controller_id: str,
        gps_id: str,
        payload: EditCellularControllerAndGpsParcelAssociationForTransportPutRequest,
        **kw,
    ) -> EditCellularControllerAndGpsParcelAssociationForTransportPutResponse:
        """
        Update a CellularController parcel and a Gps Parcel association for transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/gps/{gpsId}

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Profile Parcel ID
        :param gps_id: Gps ID
        :param payload: Gps Profile Parcel
        :returns: EditCellularControllerAndGpsParcelAssociationForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "cellularControllerId": cellular_controller_id,
            "gpsId": gps_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/gps/{gpsId}",
            return_type=EditCellularControllerAndGpsParcelAssociationForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, cellular_controller_id: str, gps_id: str, **kw):
        """
        Delete a CellularController parcel and a Gps Parcel association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/gps/{gpsId}

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Profile Parcel ID
        :param gps_id: Gps Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "cellularControllerId": cellular_controller_id,
            "gpsId": gps_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/gps/{gpsId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, cellular_controller_id: str, gps_id: str, **kw
    ) -> GetSingleSdwanTransportCellularControllerGpsPayload:
        """
        Get CellularController parcel associated Gps Parcel by gpsId for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/gps/{gpsId}

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Profile Parcel ID
        :param gps_id: Gps Parcel ID
        :returns: GetSingleSdwanTransportCellularControllerGpsPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, cellular_controller_id: str, **kw
    ) -> List[GetCellularControllerAssociatedGpsParcelsForTransportGetResponse]:
        """
        Get CellularController associated Gps Parcels for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/gps

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Feature Parcel ID
        :returns: List[GetCellularControllerAssociatedGpsParcelsForTransportGetResponse]
        """
        ...

    def get(
        self, transport_id: str, cellular_controller_id: str, gps_id: Optional[str] = None, **kw
    ) -> Union[
        List[GetCellularControllerAssociatedGpsParcelsForTransportGetResponse],
        GetSingleSdwanTransportCellularControllerGpsPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/gps/{gpsId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (cellular_controller_id, str), (gps_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "cellularControllerId": cellular_controller_id,
                "gpsId": gps_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/gps/{gpsId}",
                return_type=GetSingleSdwanTransportCellularControllerGpsPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/gps
        if self._request_adapter.param_checker(
            [(transport_id, str), (cellular_controller_id, str)], [gps_id]
        ):
            params = {
                "transportId": transport_id,
                "cellularControllerId": cellular_controller_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/gps",
                return_type=List[GetCellularControllerAssociatedGpsParcelsForTransportGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
