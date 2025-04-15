# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateNtpProfileParcelForSystemPostRequest,
    CreateNtpProfileParcelForSystemPostResponse,
    EditNtpProfileParcelForSystemPutRequest,
    EditNtpProfileParcelForSystemPutResponse,
    GetListSdwanSystemNtpPayload,
    GetSingleSdwanSystemNtpPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class NtpBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/system/ntp
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateNtpProfileParcelForSystemPostRequest, **kw
    ) -> CreateNtpProfileParcelForSystemPostResponse:
        """
        Create a Ntp Profile Parcel for System feature profile
        POST /dataservice/v1/feature-profile/sdwan/system/{systemId}/ntp

        :param system_id: Feature Profile ID
        :param payload: Ntp Profile Parcel
        :returns: CreateNtpProfileParcelForSystemPostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/ntp",
            return_type=CreateNtpProfileParcelForSystemPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self, system_id: str, ntp_id: str, payload: EditNtpProfileParcelForSystemPutRequest, **kw
    ) -> EditNtpProfileParcelForSystemPutResponse:
        """
        Update a Ntp Profile Parcel for System feature profile
        PUT /dataservice/v1/feature-profile/sdwan/system/{systemId}/ntp/{ntpId}

        :param system_id: Feature Profile ID
        :param ntp_id: Profile Parcel ID
        :param payload: Ntp Profile Parcel
        :returns: EditNtpProfileParcelForSystemPutResponse
        """
        params = {
            "systemId": system_id,
            "ntpId": ntp_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/ntp/{ntpId}",
            return_type=EditNtpProfileParcelForSystemPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, ntp_id: str, **kw):
        """
        Delete a Ntp Profile Parcel for System feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/system/{systemId}/ntp/{ntpId}

        :param system_id: Feature Profile ID
        :param ntp_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "systemId": system_id,
            "ntpId": ntp_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/ntp/{ntpId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, system_id: str, ntp_id: str, **kw) -> GetSingleSdwanSystemNtpPayload:
        """
        Get Ntp Profile Parcel by parcelId for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/ntp/{ntpId}

        :param system_id: Feature Profile ID
        :param ntp_id: Profile Parcel ID
        :returns: GetSingleSdwanSystemNtpPayload
        """
        ...

    @overload
    def get(self, system_id: str, **kw) -> GetListSdwanSystemNtpPayload:
        """
        Get Ntp Profile Parcels for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/ntp

        :param system_id: Feature Profile ID
        :returns: GetListSdwanSystemNtpPayload
        """
        ...

    def get(
        self, system_id: str, ntp_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanSystemNtpPayload, GetSingleSdwanSystemNtpPayload]:
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/ntp/{ntpId}
        if self._request_adapter.param_checker([(system_id, str), (ntp_id, str)], []):
            params = {
                "systemId": system_id,
                "ntpId": ntp_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/ntp/{ntpId}",
                return_type=GetSingleSdwanSystemNtpPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/ntp
        if self._request_adapter.param_checker([(system_id, str)], [ntp_id]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/ntp",
                return_type=GetListSdwanSystemNtpPayload,
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
