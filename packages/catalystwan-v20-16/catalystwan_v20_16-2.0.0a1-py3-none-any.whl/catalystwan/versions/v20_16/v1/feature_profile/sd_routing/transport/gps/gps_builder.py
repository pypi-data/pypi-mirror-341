# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateGpsProfileParcelForTransportPostRequest,
    CreateGpsProfileParcelForTransportPostResponse,
    EditCellularControllerAndGpsParcelAssociationForTransport1PutRequest,
    EditCellularControllerAndGpsParcelAssociationForTransport1PutResponse,
    EditGpsProfileParcelForTransportPutRequest,
    EditGpsProfileParcelForTransportPutResponse,
    GetListSdRoutingTransportGpsPayload,
    GetSingleSdRoutingTransportGpsPayload,
)


class GpsBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/gps
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, transport_id: str, payload: CreateGpsProfileParcelForTransportPostRequest, **kw
    ) -> CreateGpsProfileParcelForTransportPostResponse:
        """
        Create a GPS Profile Feature for Transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/gps

        :param transport_id: Feature Profile ID
        :param payload: GPS Profile Parcel
        :returns: CreateGpsProfileParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/gps",
            return_type=CreateGpsProfileParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, gps_id: str, **kw):
        """
        Delete a GPS Profile Feature for Transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/gps/{gpsId}

        :param transport_id: Feature Profile ID
        :param gps_id: GPS Profile Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "gpsId": gps_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/gps/{gpsId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, transport_id: str, gps_id: str, **kw) -> GetSingleSdRoutingTransportGpsPayload:
        """
        Get GPS Profile Feature by parcelId for Transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/gps/{gpsId}

        :param transport_id: Feature Profile ID
        :param gps_id: GPS Profile Parcel ID
        :returns: GetSingleSdRoutingTransportGpsPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdRoutingTransportGpsPayload:
        """
        Get GPS Profile Features for Transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/gps

        :param transport_id: Feature Profile ID
        :returns: GetListSdRoutingTransportGpsPayload
        """
        ...

    def get(
        self, transport_id: str, gps_id: Optional[str] = None, **kw
    ) -> Union[GetListSdRoutingTransportGpsPayload, GetSingleSdRoutingTransportGpsPayload]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/gps/{gpsId}
        if self._request_adapter.param_checker([(transport_id, str), (gps_id, str)], []):
            params = {
                "transportId": transport_id,
                "gpsId": gps_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/gps/{gpsId}",
                return_type=GetSingleSdRoutingTransportGpsPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/gps
        if self._request_adapter.param_checker([(transport_id, str)], [gps_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/gps",
                return_type=GetListSdRoutingTransportGpsPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @overload
    def put(
        self,
        transport_id: str,
        gps_id: str,
        payload: EditCellularControllerAndGpsParcelAssociationForTransport1PutRequest,
        cellular_controller_id: str,
        **kw,
    ) -> EditCellularControllerAndGpsParcelAssociationForTransport1PutResponse:
        """
        Update a CellularController feature and a GPS Parcel association for transport feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/{cellularControllerId}/gps/{gpsId}

        :param transport_id: Feature Profile ID
        :param gps_id: GPS Parcel ID
        :param payload: GPS Feature
        :param cellular_controller_id: Cellular Controller Feature ID
        :returns: EditCellularControllerAndGpsParcelAssociationForTransport1PutResponse
        """
        ...

    @overload
    def put(
        self,
        transport_id: str,
        gps_id: str,
        payload: EditGpsProfileParcelForTransportPutRequest,
        **kw,
    ) -> EditGpsProfileParcelForTransportPutResponse:
        """
        Update a GPS Profile Feature for Transport feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/gps/{gpsId}

        :param transport_id: Feature Profile ID
        :param gps_id: GPS Profile Parcel ID
        :param payload: GPS Profile Parcel
        :returns: EditGpsProfileParcelForTransportPutResponse
        """
        ...

    def put(
        self,
        transport_id: str,
        gps_id: str,
        payload: Union[
            EditCellularControllerAndGpsParcelAssociationForTransport1PutRequest,
            EditGpsProfileParcelForTransportPutRequest,
        ],
        cellular_controller_id: Optional[str] = None,
        **kw,
    ) -> Union[
        EditGpsProfileParcelForTransportPutResponse,
        EditCellularControllerAndGpsParcelAssociationForTransport1PutResponse,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/{cellularControllerId}/gps/{gpsId}
        if self._request_adapter.param_checker(
            [
                (transport_id, str),
                (gps_id, str),
                (payload, EditCellularControllerAndGpsParcelAssociationForTransport1PutRequest),
                (cellular_controller_id, str),
            ],
            [],
        ):
            params = {
                "transportId": transport_id,
                "gpsId": gps_id,
                "cellularControllerId": cellular_controller_id,
            }
            return self._request_adapter.request(
                "PUT",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/{cellularControllerId}/gps/{gpsId}",
                return_type=EditCellularControllerAndGpsParcelAssociationForTransport1PutResponse,
                params=params,
                payload=payload,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/gps/{gpsId}
        if self._request_adapter.param_checker(
            [
                (transport_id, str),
                (gps_id, str),
                (payload, EditGpsProfileParcelForTransportPutRequest),
            ],
            [cellular_controller_id],
        ):
            params = {
                "transportId": transport_id,
                "gpsId": gps_id,
            }
            return self._request_adapter.request(
                "PUT",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/gps/{gpsId}",
                return_type=EditGpsProfileParcelForTransportPutResponse,
                params=params,
                payload=payload,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
