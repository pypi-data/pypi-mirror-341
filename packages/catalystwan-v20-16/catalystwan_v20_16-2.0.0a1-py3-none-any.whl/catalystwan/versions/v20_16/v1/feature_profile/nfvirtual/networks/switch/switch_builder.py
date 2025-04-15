# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateNfvirtualSwitchParcelPostRequest,
    CreateNfvirtualSwitchParcelPostResponse,
    EditNfvirtualSwitchParcelPutRequest,
    EditNfvirtualSwitchParcelPutResponse,
    GetSingleNfvirtualNetworksSwitchPayload,
)


class SwitchBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/nfvirtual/networks/{networksId}/switch
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, networks_id: str, payload: CreateNfvirtualSwitchParcelPostRequest, **kw
    ) -> CreateNfvirtualSwitchParcelPostResponse:
        """
        Create Switch Profile config for Networks feature profile
        POST /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/switch

        :param networks_id: Feature Profile ID
        :param payload: Switch config Profile Parcel
        :returns: CreateNfvirtualSwitchParcelPostResponse
        """
        params = {
            "networksId": networks_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/switch",
            return_type=CreateNfvirtualSwitchParcelPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def get(
        self, networks_id: str, switch_id: str, **kw
    ) -> GetSingleNfvirtualNetworksSwitchPayload:
        """
        Get Switch Profile Parcels for Networks feature profile
        GET /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/switch/{switchId}

        :param networks_id: Feature Profile ID
        :param switch_id: Profile Parcel ID
        :returns: GetSingleNfvirtualNetworksSwitchPayload
        """
        params = {
            "networksId": networks_id,
            "switchId": switch_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/switch/{switchId}",
            return_type=GetSingleNfvirtualNetworksSwitchPayload,
            params=params,
            **kw,
        )

    def put(
        self, networks_id: str, switch_id: str, payload: EditNfvirtualSwitchParcelPutRequest, **kw
    ) -> EditNfvirtualSwitchParcelPutResponse:
        """
        Edit a Switch Profile Parcel for networks feature profile
        PUT /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/switch/{switchId}

        :param networks_id: Feature Profile ID
        :param switch_id: Profile Parcel ID
        :param payload: Switch Profile Parcel
        :returns: EditNfvirtualSwitchParcelPutResponse
        """
        params = {
            "networksId": networks_id,
            "switchId": switch_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/switch/{switchId}",
            return_type=EditNfvirtualSwitchParcelPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, networks_id: str, switch_id: str, **kw):
        """
        Delete Switch Profile config for Networks feature profile
        DELETE /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/switch/{switchId}

        :param networks_id: Feature Profile ID
        :param switch_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "networksId": networks_id,
            "switchId": switch_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/switch/{switchId}",
            params=params,
            **kw,
        )
