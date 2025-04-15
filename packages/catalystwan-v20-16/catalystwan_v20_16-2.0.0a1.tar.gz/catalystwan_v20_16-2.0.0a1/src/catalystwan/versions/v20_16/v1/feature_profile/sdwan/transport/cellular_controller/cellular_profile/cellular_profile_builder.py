# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateCellularControllerAndCellularProfileParcelAssociationForTransportPostRequest,
    CreateCellularControllerAndCellularProfileParcelAssociationForTransportPostResponse,
    EditCellularControllerAndCellularProfileParcelAssociationForTransportPutRequest,
    EditCellularControllerAndCellularProfileParcelAssociationForTransportPutResponse,
    GetCellularControllerAssociatedCellularProfileParcelsForTransportGetResponse,
    GetSingleSdwanTransportCellularControllerCellularProfilePayload,
)


class CellularProfileBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        cellular_controller_id: str,
        payload: CreateCellularControllerAndCellularProfileParcelAssociationForTransportPostRequest,
        **kw,
    ) -> CreateCellularControllerAndCellularProfileParcelAssociationForTransportPostResponse:
        """
        Associate a cellularcontroller parcel with a cellularprofile Parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Cellular Controller Profile Parcel ID
        :param payload: Cellular Profile Profile Parcel Id
        :returns: CreateCellularControllerAndCellularProfileParcelAssociationForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "cellularControllerId": cellular_controller_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile",
            return_type=CreateCellularControllerAndCellularProfileParcelAssociationForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        cellular_controller_id: str,
        cellular_profile_id: str,
        payload: EditCellularControllerAndCellularProfileParcelAssociationForTransportPutRequest,
        **kw,
    ) -> EditCellularControllerAndCellularProfileParcelAssociationForTransportPutResponse:
        """
        Update a CellularController parcel and a CellularProfile Parcel association for transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile/{cellularProfileId}

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Profile Parcel ID
        :param cellular_profile_id: Cellular Profile ID
        :param payload: Cellular Profile Profile Parcel
        :returns: EditCellularControllerAndCellularProfileParcelAssociationForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "cellularControllerId": cellular_controller_id,
            "cellularProfileId": cellular_profile_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile/{cellularProfileId}",
            return_type=EditCellularControllerAndCellularProfileParcelAssociationForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(
        self, transport_id: str, cellular_controller_id: str, cellular_profile_id: str, **kw
    ):
        """
        Delete a CellularController parcel and a CellularProfile Parcel association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile/{cellularProfileId}

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Profile Parcel ID
        :param cellular_profile_id: Cellular Profile Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "cellularControllerId": cellular_controller_id,
            "cellularProfileId": cellular_profile_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile/{cellularProfileId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, cellular_controller_id: str, cellular_profile_id: str, **kw
    ) -> GetSingleSdwanTransportCellularControllerCellularProfilePayload:
        """
        Get CellularController parcel associated CellularProfile Parcel by cellularProfileId for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile/{cellularProfileId}

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Profile Parcel ID
        :param cellular_profile_id: Cellular Profile Parcel ID
        :returns: GetSingleSdwanTransportCellularControllerCellularProfilePayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, cellular_controller_id: str, **kw
    ) -> List[GetCellularControllerAssociatedCellularProfileParcelsForTransportGetResponse]:
        """
        Get CellularController associated Cellular Profile Parcels for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Feature Parcel ID
        :returns: List[GetCellularControllerAssociatedCellularProfileParcelsForTransportGetResponse]
        """
        ...

    def get(
        self,
        transport_id: str,
        cellular_controller_id: str,
        cellular_profile_id: Optional[str] = None,
        **kw,
    ) -> Union[
        List[GetCellularControllerAssociatedCellularProfileParcelsForTransportGetResponse],
        GetSingleSdwanTransportCellularControllerCellularProfilePayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile/{cellularProfileId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (cellular_controller_id, str), (cellular_profile_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "cellularControllerId": cellular_controller_id,
                "cellularProfileId": cellular_profile_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile/{cellularProfileId}",
                return_type=GetSingleSdwanTransportCellularControllerCellularProfilePayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile
        if self._request_adapter.param_checker(
            [(transport_id, str), (cellular_controller_id, str)], [cellular_profile_id]
        ):
            params = {
                "transportId": transport_id,
                "cellularControllerId": cellular_controller_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile",
                return_type=List[
                    GetCellularControllerAssociatedCellularProfileParcelsForTransportGetResponse
                ],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
