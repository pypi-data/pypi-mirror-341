# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateCellularProfileParcelForTransportPostRequest,
    CreateCellularProfileParcelForTransportPostResponse,
    EditCellularProfileParcelForTransportPutRequest,
    EditCellularProfileParcelForTransportPutResponse,
    GetListSdRoutingTransportCellularProfilePayload,
    GetSingleSdRoutingTransportCellularProfilePayload,
)


class CellularProfileBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/cellular-profile
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, transport_id: str, payload: CreateCellularProfileParcelForTransportPostRequest, **kw
    ) -> CreateCellularProfileParcelForTransportPostResponse:
        """
        Create a Cellular Profile Feature for Transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-profile

        :param transport_id: Feature Profile ID
        :param payload: Cellular Profile Parcel
        :returns: CreateCellularProfileParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-profile",
            return_type=CreateCellularProfileParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        cellular_profile_id: str,
        payload: EditCellularProfileParcelForTransportPutRequest,
        **kw,
    ) -> EditCellularProfileParcelForTransportPutResponse:
        """
        Update a Cellular Profile Feature for Transport feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-profile/{cellularProfileId}

        :param transport_id: Feature Profile ID
        :param cellular_profile_id: Cellular Profile Feature ID
        :param payload: Cellular Profile Parcel
        :returns: EditCellularProfileParcelForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "cellularProfileId": cellular_profile_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-profile/{cellularProfileId}",
            return_type=EditCellularProfileParcelForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, cellular_profile_id: str, **kw):
        """
        Delete a Cellular Profile Feature for Transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-profile/{cellularProfileId}

        :param transport_id: Feature Profile ID
        :param cellular_profile_id: Cellular Profile Feature ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "cellularProfileId": cellular_profile_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-profile/{cellularProfileId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, cellular_profile_id: str, **kw
    ) -> GetSingleSdRoutingTransportCellularProfilePayload:
        """
        Get Cellular Profile Feature by parcelId for Transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-profile/{cellularProfileId}

        :param transport_id: Feature Profile ID
        :param cellular_profile_id: Cellular Profile Feature ID
        :returns: GetSingleSdRoutingTransportCellularProfilePayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdRoutingTransportCellularProfilePayload:
        """
        Get Cellular Profile Features for Transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-profile

        :param transport_id: Feature Profile ID
        :returns: GetListSdRoutingTransportCellularProfilePayload
        """
        ...

    def get(
        self, transport_id: str, cellular_profile_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingTransportCellularProfilePayload,
        GetSingleSdRoutingTransportCellularProfilePayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-profile/{cellularProfileId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (cellular_profile_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "cellularProfileId": cellular_profile_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-profile/{cellularProfileId}",
                return_type=GetSingleSdRoutingTransportCellularProfilePayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-profile
        if self._request_adapter.param_checker([(transport_id, str)], [cellular_profile_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-profile",
                return_type=GetListSdRoutingTransportCellularProfilePayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
