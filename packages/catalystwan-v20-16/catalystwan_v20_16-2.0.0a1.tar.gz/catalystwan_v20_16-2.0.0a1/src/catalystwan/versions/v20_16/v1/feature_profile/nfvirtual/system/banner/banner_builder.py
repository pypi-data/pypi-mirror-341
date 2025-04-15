# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateNfvirtualBannerParcelPostRequest,
    CreateNfvirtualBannerParcelPostResponse,
    EditNfvirtualBannerParcelPutRequest,
    EditNfvirtualBannerParcelPutResponse,
    GetSingleNfvirtualSystemBannerPayload,
)


class BannerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/nfvirtual/system/{systemId}/banner
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateNfvirtualBannerParcelPostRequest, **kw
    ) -> CreateNfvirtualBannerParcelPostResponse:
        """
        Create Banner Profile Parcel for System feature profile
        POST /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/banner

        :param system_id: Feature Profile ID
        :param payload: Banner config Profile Parcel
        :returns: CreateNfvirtualBannerParcelPostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/banner",
            return_type=CreateNfvirtualBannerParcelPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def get(self, system_id: str, banner_id: str, **kw) -> GetSingleNfvirtualSystemBannerPayload:
        """
        Get Banner Profile Parcels for System feature profile
        GET /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/banner/{bannerId}

        :param system_id: Feature Profile ID
        :param banner_id: Profile Parcel ID
        :returns: GetSingleNfvirtualSystemBannerPayload
        """
        params = {
            "systemId": system_id,
            "bannerId": banner_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/banner/{bannerId}",
            return_type=GetSingleNfvirtualSystemBannerPayload,
            params=params,
            **kw,
        )

    def put(
        self, system_id: str, banner_id: str, payload: EditNfvirtualBannerParcelPutRequest, **kw
    ) -> EditNfvirtualBannerParcelPutResponse:
        """
        Edit a  Banner Profile Parcel for System feature profile
        PUT /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/banner/{bannerId}

        :param system_id: Feature Profile ID
        :param banner_id: Profile Parcel ID
        :param payload: Banner Profile Parcel
        :returns: EditNfvirtualBannerParcelPutResponse
        """
        params = {
            "systemId": system_id,
            "bannerId": banner_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/banner/{bannerId}",
            return_type=EditNfvirtualBannerParcelPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, banner_id: str, **kw):
        """
        Delete a Banner Profile Parcel for System feature profile
        DELETE /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/banner/{bannerId}

        :param system_id: Feature Profile ID
        :param banner_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "systemId": system_id,
            "bannerId": banner_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/banner/{bannerId}",
            params=params,
            **kw,
        )
