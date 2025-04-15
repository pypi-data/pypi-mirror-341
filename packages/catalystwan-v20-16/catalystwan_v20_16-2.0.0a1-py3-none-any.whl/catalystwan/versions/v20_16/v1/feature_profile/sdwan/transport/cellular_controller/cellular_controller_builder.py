# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateCellularControllerProfileParcelForTransportPostRequest,
    CreateCellularControllerProfileParcelForTransportPostResponse,
    EditCellularControllerProfileParcelForTransportPutRequest,
    EditCellularControllerProfileParcelForTransportPutResponse,
    GetListSdwanTransportCellularControllerPayload,
    GetSingleSdwanTransportCellularControllerPayload,
)

if TYPE_CHECKING:
    from .cellular_profile.cellular_profile_builder import CellularProfileBuilder
    from .gps.gps_builder import GpsBuilder
    from .schema.schema_builder import SchemaBuilder


class CellularControllerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/cellular-controller
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        payload: CreateCellularControllerProfileParcelForTransportPostRequest,
        **kw,
    ) -> CreateCellularControllerProfileParcelForTransportPostResponse:
        """
        Create a Cellular Controller Profile Parcel for Transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller

        :param transport_id: Feature Profile ID
        :param payload: Cellular Controller Profile Parcel
        :returns: CreateCellularControllerProfileParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller",
            return_type=CreateCellularControllerProfileParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        cellular_controller_id: str,
        payload: EditCellularControllerProfileParcelForTransportPutRequest,
        **kw,
    ) -> EditCellularControllerProfileParcelForTransportPutResponse:
        """
        Update a Cellular Controller Profile Parcel for Transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Profile Parcel ID
        :param payload: Cellular Controller Profile Parcel
        :returns: EditCellularControllerProfileParcelForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "cellularControllerId": cellular_controller_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}",
            return_type=EditCellularControllerProfileParcelForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, cellular_controller_id: str, **kw):
        """
        Delete a Cellular Controller Profile Parcel for Transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "cellularControllerId": cellular_controller_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, cellular_controller_id: str, **kw
    ) -> GetSingleSdwanTransportCellularControllerPayload:
        """
        Get Cellular Controller Profile Parcel by parcelId for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Profile Parcel ID
        :returns: GetSingleSdwanTransportCellularControllerPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdwanTransportCellularControllerPayload:
        """
        Get Cellular Controller Profile Parcels for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller

        :param transport_id: Feature Profile ID
        :returns: GetListSdwanTransportCellularControllerPayload
        """
        ...

    def get(
        self, transport_id: str, cellular_controller_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanTransportCellularControllerPayload,
        GetSingleSdwanTransportCellularControllerPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (cellular_controller_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "cellularControllerId": cellular_controller_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}",
                return_type=GetSingleSdwanTransportCellularControllerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller
        if self._request_adapter.param_checker([(transport_id, str)], [cellular_controller_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller",
                return_type=GetListSdwanTransportCellularControllerPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def cellular_profile(self) -> CellularProfileBuilder:
        """
        The cellular-profile property
        """
        from .cellular_profile.cellular_profile_builder import CellularProfileBuilder

        return CellularProfileBuilder(self._request_adapter)

    @property
    def gps(self) -> GpsBuilder:
        """
        The gps property
        """
        from .gps.gps_builder import GpsBuilder

        return GpsBuilder(self._request_adapter)

    @property
    def schema(self) -> SchemaBuilder:
        """
        The schema property
        """
        from .schema.schema_builder import SchemaBuilder

        return SchemaBuilder(self._request_adapter)
