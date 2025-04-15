# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateNfvirtualRoutesParcelPostRequest,
    CreateNfvirtualRoutesParcelPostResponse,
    EditNfvirtualRoutesParcelPutRequest,
    EditNfvirtualRoutesParcelPutResponse,
    GetSingleNfvirtualNetworksRoutesPayload,
)


class RoutesBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/nfvirtual/networks/{networksId}/routes
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, networks_id: str, payload: CreateNfvirtualRoutesParcelPostRequest, **kw
    ) -> CreateNfvirtualRoutesParcelPostResponse:
        """
        Create Routes Profile config for Networks feature profile
        POST /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/routes

        :param networks_id: Feature Profile ID
        :param payload: Routes config Profile Parcel
        :returns: CreateNfvirtualRoutesParcelPostResponse
        """
        params = {
            "networksId": networks_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/routes",
            return_type=CreateNfvirtualRoutesParcelPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def get(
        self, networks_id: str, routes_id: str, **kw
    ) -> GetSingleNfvirtualNetworksRoutesPayload:
        """
        Get Routes Profile Parcels for Networks feature profile
        GET /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/routes/{routesId}

        :param networks_id: Feature Profile ID
        :param routes_id: Profile Parcel ID
        :returns: GetSingleNfvirtualNetworksRoutesPayload
        """
        params = {
            "networksId": networks_id,
            "routesId": routes_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/routes/{routesId}",
            return_type=GetSingleNfvirtualNetworksRoutesPayload,
            params=params,
            **kw,
        )

    def put(
        self, networks_id: str, routes_id: str, payload: EditNfvirtualRoutesParcelPutRequest, **kw
    ) -> EditNfvirtualRoutesParcelPutResponse:
        """
        Edit a Routes Profile Parcel for networks feature profile
        PUT /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/routes/{routesId}

        :param networks_id: Feature Profile ID
        :param routes_id: Profile Parcel ID
        :param payload: Routes Profile Parcel
        :returns: EditNfvirtualRoutesParcelPutResponse
        """
        params = {
            "networksId": networks_id,
            "routesId": routes_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/routes/{routesId}",
            return_type=EditNfvirtualRoutesParcelPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, networks_id: str, routes_id: str, **kw):
        """
        Delete Routes Profile config for Networks feature profile
        DELETE /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/routes/{routesId}

        :param networks_id: Feature Profile ID
        :param routes_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "networksId": networks_id,
            "routesId": routes_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/routes/{routesId}",
            params=params,
            **kw,
        )
