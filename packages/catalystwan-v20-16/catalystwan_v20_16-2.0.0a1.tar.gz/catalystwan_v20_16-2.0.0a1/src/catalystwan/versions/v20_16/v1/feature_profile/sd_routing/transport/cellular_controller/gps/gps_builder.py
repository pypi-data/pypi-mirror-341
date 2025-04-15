# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateCellularControllerAndGpsParcelAssociationForTransport1PostRequest,
    CreateCellularControllerAndGpsParcelAssociationForTransport1PostResponse,
    GetCellularControllerAssociatedGpsParcelsForTransport1GetResponse,
    GetSingleSdRoutingTransportCellularControllerGpsPayload,
)


class GpsBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/gps
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        cellular_controller_id: str,
        payload: CreateCellularControllerAndGpsParcelAssociationForTransport1PostRequest,
        **kw,
    ) -> CreateCellularControllerAndGpsParcelAssociationForTransport1PostResponse:
        """
        Associate a cellularcontroller feature with a GPS Parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/gps

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Cellular Controller Feature ID
        :param payload: GPS Profile Parcel Id
        :returns: CreateCellularControllerAndGpsParcelAssociationForTransport1PostResponse
        """
        params = {
            "transportId": transport_id,
            "cellularControllerId": cellular_controller_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/gps",
            return_type=CreateCellularControllerAndGpsParcelAssociationForTransport1PostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, cellular_controller_id: str, gps_id: str, **kw):
        """
        Delete a CellularController feature and a GPS Feature association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/gps/{gpsId}

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Cellular Controller Feature ID
        :param gps_id: GPS Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "cellularControllerId": cellular_controller_id,
            "gpsId": gps_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/gps/{gpsId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, cellular_controller_id: str, gps_id: str, **kw
    ) -> GetSingleSdRoutingTransportCellularControllerGpsPayload:
        """
        Get CellularController feature associated GPS Feature by gpsId for transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/gps/{gpsId}

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Cellular Controller Feature ID
        :param gps_id: GPS Parcel ID
        :returns: GetSingleSdRoutingTransportCellularControllerGpsPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, cellular_controller_id: str, **kw
    ) -> List[GetCellularControllerAssociatedGpsParcelsForTransport1GetResponse]:
        """
        Get CellularController associated GPS Features for transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/gps

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Cellular Controller Feature ID
        :returns: List[GetCellularControllerAssociatedGpsParcelsForTransport1GetResponse]
        """
        ...

    def get(
        self, transport_id: str, cellular_controller_id: str, gps_id: Optional[str] = None, **kw
    ) -> Union[
        List[GetCellularControllerAssociatedGpsParcelsForTransport1GetResponse],
        GetSingleSdRoutingTransportCellularControllerGpsPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/gps/{gpsId}
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
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/gps/{gpsId}",
                return_type=GetSingleSdRoutingTransportCellularControllerGpsPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/gps
        if self._request_adapter.param_checker(
            [(transport_id, str), (cellular_controller_id, str)], [gps_id]
        ):
            params = {
                "transportId": transport_id,
                "cellularControllerId": cellular_controller_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/gps",
                return_type=List[GetCellularControllerAssociatedGpsParcelsForTransport1GetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
