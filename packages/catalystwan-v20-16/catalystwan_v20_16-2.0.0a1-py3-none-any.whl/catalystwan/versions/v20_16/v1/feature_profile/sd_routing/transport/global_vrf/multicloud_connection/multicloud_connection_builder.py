# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateTransportGlobalVrfAndMulticloudConnectionParcelAssociationPostRequest,
    CreateTransportGlobalVrfAndMulticloudConnectionParcelAssociationPostResponse,
)


class MulticloudConnectionBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/multicloud-connection
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        vrf_id: str,
        payload: CreateTransportGlobalVrfAndMulticloudConnectionParcelAssociationPostRequest,
        **kw,
    ) -> CreateTransportGlobalVrfAndMulticloudConnectionParcelAssociationPostResponse:
        """
        Associate a Global VRF parcel with a Multicloud Connection Parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/multicloud-connection

        :param transport_id: Feature Profile ID
        :param vrf_id: Global VRF Profile Parcel ID
        :param payload: Multicloud Connection Profile Parcel Id
        :returns: CreateTransportGlobalVrfAndMulticloudConnectionParcelAssociationPostResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/multicloud-connection",
            return_type=CreateTransportGlobalVrfAndMulticloudConnectionParcelAssociationPostResponse,
            params=params,
            payload=payload,
            **kw,
        )
