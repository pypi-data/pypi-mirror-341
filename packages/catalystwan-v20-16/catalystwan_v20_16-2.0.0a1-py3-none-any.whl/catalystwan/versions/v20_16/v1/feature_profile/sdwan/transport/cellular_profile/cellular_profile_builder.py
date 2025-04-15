# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateCellularProfileProfileParcelForTransportPostRequest,
    CreateCellularProfileProfileParcelForTransportPostResponse,
    EditCellularProfileProfileParcelForTransportPutRequest,
    EditCellularProfileProfileParcelForTransportPutResponse,
    GetListSdwanTransportCellularProfilePayload,
    GetSingleSdwanTransportCellularProfilePayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class CellularProfileBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/cellular-profile
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        payload: CreateCellularProfileProfileParcelForTransportPostRequest,
        **kw,
    ) -> CreateCellularProfileProfileParcelForTransportPostResponse:
        """
        Create a Cellular Profile Profile Parcel for Transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-profile

        :param transport_id: Feature Profile ID
        :param payload: Cellular Profile Profile Parcel
        :returns: CreateCellularProfileProfileParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-profile",
            return_type=CreateCellularProfileProfileParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        cellular_profile_id: str,
        payload: EditCellularProfileProfileParcelForTransportPutRequest,
        **kw,
    ) -> EditCellularProfileProfileParcelForTransportPutResponse:
        """
        Update a Cellular Profile Profile Parcel for Transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-profile/{cellularProfileId}

        :param transport_id: Feature Profile ID
        :param cellular_profile_id: Profile Parcel ID
        :param payload: Cellular Profile Profile Parcel
        :returns: EditCellularProfileProfileParcelForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "cellularProfileId": cellular_profile_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-profile/{cellularProfileId}",
            return_type=EditCellularProfileProfileParcelForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, cellular_profile_id: str, **kw):
        """
        Delete a Cellular Profile Profile Parcel for Transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-profile/{cellularProfileId}

        :param transport_id: Feature Profile ID
        :param cellular_profile_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "cellularProfileId": cellular_profile_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-profile/{cellularProfileId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, cellular_profile_id: str, **kw
    ) -> GetSingleSdwanTransportCellularProfilePayload:
        """
        Get Cellular Profile Profile Parcel by parcelId for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-profile/{cellularProfileId}

        :param transport_id: Feature Profile ID
        :param cellular_profile_id: Profile Parcel ID
        :returns: GetSingleSdwanTransportCellularProfilePayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdwanTransportCellularProfilePayload:
        """
        Get Cellular Profile Profile Parcels for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-profile

        :param transport_id: Feature Profile ID
        :returns: GetListSdwanTransportCellularProfilePayload
        """
        ...

    def get(
        self, transport_id: str, cellular_profile_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanTransportCellularProfilePayload, GetSingleSdwanTransportCellularProfilePayload
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-profile/{cellularProfileId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (cellular_profile_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "cellularProfileId": cellular_profile_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-profile/{cellularProfileId}",
                return_type=GetSingleSdwanTransportCellularProfilePayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-profile
        if self._request_adapter.param_checker([(transport_id, str)], [cellular_profile_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-profile",
                return_type=GetListSdwanTransportCellularProfilePayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def schema(self) -> SchemaBuilder:
        """
        The schema property
        """
        from .schema.schema_builder import SchemaBuilder

        return SchemaBuilder(self._request_adapter)
