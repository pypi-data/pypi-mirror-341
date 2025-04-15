# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateCellularControllerAndCellularProfileParcelAssociationForTransport1PostRequest,
    CreateCellularControllerAndCellularProfileParcelAssociationForTransport1PostResponse,
    EditCellularControllerAndCellularProfileParcelAssociationForTransport1PutRequest,
    EditCellularControllerAndCellularProfileParcelAssociationForTransport1PutResponse,
    GetCellularControllerAssociatedCellularProfileParcelsForTransport1GetResponse,
    GetSingleSdRoutingTransportCellularControllerCellularProfilePayload,
)


class CellularProfileBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        cellular_controller_id: str,
        payload: CreateCellularControllerAndCellularProfileParcelAssociationForTransport1PostRequest,
        **kw,
    ) -> CreateCellularControllerAndCellularProfileParcelAssociationForTransport1PostResponse:
        """
        Associate a cellularcontroller feature with a cellularprofile Parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Cellular Controller Feature ID
        :param payload: Cellular Profile Parcel Id
        :returns: CreateCellularControllerAndCellularProfileParcelAssociationForTransport1PostResponse
        """
        params = {
            "transportId": transport_id,
            "cellularControllerId": cellular_controller_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile",
            return_type=CreateCellularControllerAndCellularProfileParcelAssociationForTransport1PostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        cellular_controller_id: str,
        cellular_profile_id: str,
        payload: EditCellularControllerAndCellularProfileParcelAssociationForTransport1PutRequest,
        **kw,
    ) -> EditCellularControllerAndCellularProfileParcelAssociationForTransport1PutResponse:
        """
        Update a CellularController feature and a CellularProfile Parcel association for transport feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile/{cellularProfileId}

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Cellular Controller Feature ID
        :param cellular_profile_id: Cellular Profile ID
        :param payload: Cellular Profile Parcel
        :returns: EditCellularControllerAndCellularProfileParcelAssociationForTransport1PutResponse
        """
        params = {
            "transportId": transport_id,
            "cellularControllerId": cellular_controller_id,
            "cellularProfileId": cellular_profile_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile/{cellularProfileId}",
            return_type=EditCellularControllerAndCellularProfileParcelAssociationForTransport1PutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(
        self, transport_id: str, cellular_controller_id: str, cellular_profile_id: str, **kw
    ):
        """
        Delete a CellularController feature and a CellularProfile Parcel association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile/{cellularProfileId}

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Cellular Controller Feature ID
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
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile/{cellularProfileId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, cellular_controller_id: str, cellular_profile_id: str, **kw
    ) -> GetSingleSdRoutingTransportCellularControllerCellularProfilePayload:
        """
        Get CellularController feature associated CellularProfile Parcel by cellularProfileId for transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile/{cellularProfileId}

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Cellular Controller Feature ID
        :param cellular_profile_id: Cellular Profile Parcel ID
        :returns: GetSingleSdRoutingTransportCellularControllerCellularProfilePayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, cellular_controller_id: str, **kw
    ) -> List[GetCellularControllerAssociatedCellularProfileParcelsForTransport1GetResponse]:
        """
        Get CellularController associated Cellular Profile Features for transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile

        :param transport_id: Feature Profile ID
        :param cellular_controller_id: Cellular Controller Feature ID
        :returns: List[GetCellularControllerAssociatedCellularProfileParcelsForTransport1GetResponse]
        """
        ...

    def get(
        self,
        transport_id: str,
        cellular_controller_id: str,
        cellular_profile_id: Optional[str] = None,
        **kw,
    ) -> Union[
        List[GetCellularControllerAssociatedCellularProfileParcelsForTransport1GetResponse],
        GetSingleSdRoutingTransportCellularControllerCellularProfilePayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile/{cellularProfileId}
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
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile/{cellularProfileId}",
                return_type=GetSingleSdRoutingTransportCellularControllerCellularProfilePayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile
        if self._request_adapter.param_checker(
            [(transport_id, str), (cellular_controller_id, str)], [cellular_profile_id]
        ):
            params = {
                "transportId": transport_id,
                "cellularControllerId": cellular_controller_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/cellular-controller/{cellularControllerId}/cellular-profile",
                return_type=List[
                    GetCellularControllerAssociatedCellularProfileParcelsForTransport1GetResponse
                ],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
