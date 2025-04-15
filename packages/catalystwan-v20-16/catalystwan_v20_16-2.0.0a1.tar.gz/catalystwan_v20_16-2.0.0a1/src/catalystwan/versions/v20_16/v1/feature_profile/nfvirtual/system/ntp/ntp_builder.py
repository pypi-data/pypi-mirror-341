# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateNfvirtualNtpParcelPostRequest,
    CreateNfvirtualNtpParcelPostResponse,
    EditNfvirtualNtpParcelPutRequest,
    EditNfvirtualNtpParcelPutResponse,
    GetSingleNfvirtualSystemNtpPayload,
)


class NtpBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/nfvirtual/system/{systemId}/ntp
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateNfvirtualNtpParcelPostRequest, **kw
    ) -> CreateNfvirtualNtpParcelPostResponse:
        """
        Create NTP Profile Parcel for System feature profile
        POST /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/ntp

        :param system_id: Feature Profile ID
        :param payload: NTP config Profile Parcel
        :returns: CreateNfvirtualNtpParcelPostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/ntp",
            return_type=CreateNfvirtualNtpParcelPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def get(self, system_id: str, ntp_id: str, **kw) -> GetSingleNfvirtualSystemNtpPayload:
        """
        Get NTP Profile Parcels for System feature profile
        GET /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/ntp/{ntpId}

        :param system_id: Feature Profile ID
        :param ntp_id: Profile Parcel ID
        :returns: GetSingleNfvirtualSystemNtpPayload
        """
        params = {
            "systemId": system_id,
            "ntpId": ntp_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/ntp/{ntpId}",
            return_type=GetSingleNfvirtualSystemNtpPayload,
            params=params,
            **kw,
        )

    def put(
        self, system_id: str, ntp_id: str, payload: EditNfvirtualNtpParcelPutRequest, **kw
    ) -> EditNfvirtualNtpParcelPutResponse:
        """
        Edit a  NTP Profile Parcel for System feature profile
        PUT /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/ntp/{ntpId}

        :param system_id: Feature Profile ID
        :param ntp_id: Profile Parcel ID
        :param payload: NTP Profile Parcel
        :returns: EditNfvirtualNtpParcelPutResponse
        """
        params = {
            "systemId": system_id,
            "ntpId": ntp_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/ntp/{ntpId}",
            return_type=EditNfvirtualNtpParcelPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, ntp_id: str, **kw):
        """
        Delete a NTP Profile Parcel for System feature profile
        DELETE /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/ntp/{ntpId}

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
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/ntp/{ntpId}",
            params=params,
            **kw,
        )
