# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateBannerProfileParcelForSystemPostRequest,
    CreateBannerProfileParcelForSystemPostResponse,
    EditBannerProfileParcelForSystemPutRequest,
    EditBannerProfileParcelForSystemPutResponse,
    GetListSdwanSystemBannerPayload,
    GetSingleSdwanSystemBannerPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class BannerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/system/banner
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateBannerProfileParcelForSystemPostRequest, **kw
    ) -> CreateBannerProfileParcelForSystemPostResponse:
        """
        Create a Banner Profile Parcel for System feature profile
        POST /dataservice/v1/feature-profile/sdwan/system/{systemId}/banner

        :param system_id: Feature Profile ID
        :param payload: Banner Profile Parcel
        :returns: CreateBannerProfileParcelForSystemPostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/banner",
            return_type=CreateBannerProfileParcelForSystemPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        system_id: str,
        banner_id: str,
        payload: EditBannerProfileParcelForSystemPutRequest,
        **kw,
    ) -> EditBannerProfileParcelForSystemPutResponse:
        """
        Update a Banner Profile Parcel for System feature profile
        PUT /dataservice/v1/feature-profile/sdwan/system/{systemId}/banner/{bannerId}

        :param system_id: Feature Profile ID
        :param banner_id: Profile Parcel ID
        :param payload: Banner Profile Parcel
        :returns: EditBannerProfileParcelForSystemPutResponse
        """
        params = {
            "systemId": system_id,
            "bannerId": banner_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/banner/{bannerId}",
            return_type=EditBannerProfileParcelForSystemPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, banner_id: str, **kw):
        """
        Delete a Banner Profile Parcel for System feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/system/{systemId}/banner/{bannerId}

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
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/banner/{bannerId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, system_id: str, banner_id: str, **kw) -> GetSingleSdwanSystemBannerPayload:
        """
        Get Banner Profile Parcel by parcelId for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/banner/{bannerId}

        :param system_id: Feature Profile ID
        :param banner_id: Profile Parcel ID
        :returns: GetSingleSdwanSystemBannerPayload
        """
        ...

    @overload
    def get(self, system_id: str, **kw) -> GetListSdwanSystemBannerPayload:
        """
        Get Banner Profile Parcels for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/banner

        :param system_id: Feature Profile ID
        :returns: GetListSdwanSystemBannerPayload
        """
        ...

    def get(
        self, system_id: str, banner_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanSystemBannerPayload, GetSingleSdwanSystemBannerPayload]:
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/banner/{bannerId}
        if self._request_adapter.param_checker([(system_id, str), (banner_id, str)], []):
            params = {
                "systemId": system_id,
                "bannerId": banner_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/banner/{bannerId}",
                return_type=GetSingleSdwanSystemBannerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/banner
        if self._request_adapter.param_checker([(system_id, str)], [banner_id]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/banner",
                return_type=GetListSdwanSystemBannerPayload,
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
