# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSigSecurityProfileParcel1PostRequest,
    CreateSigSecurityProfileParcel1PostResponse,
    EditSigSecurityProfileParcel1PutRequest,
    EditSigSecurityProfileParcel1PutResponse,
    GetListSdwanSigSecuritySigPayload,
    GetSingleSdwanSigSecuritySigPayload,
)


class SigBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/sig-security/{sigSecurityId}/sig
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, sig_security_id: str, payload: CreateSigSecurityProfileParcel1PostRequest, **kw
    ) -> CreateSigSecurityProfileParcel1PostResponse:
        """
        Create Parcel for Sig Security Policy
        POST /dataservice/v1/feature-profile/sdwan/sig-security/{sigSecurityId}/sig

        :param sig_security_id: Feature Profile ID
        :param payload: Sig Security Profile Parcel
        :returns: CreateSigSecurityProfileParcel1PostResponse
        """
        params = {
            "sigSecurityId": sig_security_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/sig-security/{sigSecurityId}/sig",
            return_type=CreateSigSecurityProfileParcel1PostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        sig_security_id: str,
        sig_security_profile_parcel_id: str,
        payload: EditSigSecurityProfileParcel1PutRequest,
        **kw,
    ) -> EditSigSecurityProfileParcel1PutResponse:
        """
        Update a Sig Security Profile Parcel
        PUT /dataservice/v1/feature-profile/sdwan/sig-security/{sigSecurityId}/sig/{sigSecurityProfileParcelId}

        :param sig_security_id: Feature Profile ID
        :param sig_security_profile_parcel_id: Profile Parcel ID
        :param payload: Sig Security Profile Parcel
        :returns: EditSigSecurityProfileParcel1PutResponse
        """
        params = {
            "sigSecurityId": sig_security_id,
            "sigSecurityProfileParcelId": sig_security_profile_parcel_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/sig-security/{sigSecurityId}/sig/{sigSecurityProfileParcelId}",
            return_type=EditSigSecurityProfileParcel1PutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, sig_security_id: str, sig_security_profile_parcel_id: str, **kw):
        """
        Delete a SigSecurity Profile Parcel
        DELETE /dataservice/v1/feature-profile/sdwan/sig-security/{sigSecurityId}/sig/{sigSecurityProfileParcelId}

        :param sig_security_id: Feature Profile ID
        :param sig_security_profile_parcel_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "sigSecurityId": sig_security_id,
            "sigSecurityProfileParcelId": sig_security_profile_parcel_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/sig-security/{sigSecurityId}/sig/{sigSecurityProfileParcelId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, sig_security_id: str, sig_security_profile_parcel_id: str, **kw
    ) -> GetSingleSdwanSigSecuritySigPayload:
        """
        Get SigSecurity Profile Parcel by parcelId
        GET /dataservice/v1/feature-profile/sdwan/sig-security/{sigSecurityId}/sig/{sigSecurityProfileParcelId}

        :param sig_security_id: Feature Profile ID
        :param sig_security_profile_parcel_id: Profile Parcel ID
        :returns: GetSingleSdwanSigSecuritySigPayload
        """
        ...

    @overload
    def get(self, sig_security_id: str, **kw) -> GetListSdwanSigSecuritySigPayload:
        """
        Get Sig Security Profile Parcels for a given ParcelType
        GET /dataservice/v1/feature-profile/sdwan/sig-security/{sigSecurityId}/sig

        :param sig_security_id: Feature Profile ID
        :returns: GetListSdwanSigSecuritySigPayload
        """
        ...

    def get(
        self, sig_security_id: str, sig_security_profile_parcel_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanSigSecuritySigPayload, GetSingleSdwanSigSecuritySigPayload]:
        # /dataservice/v1/feature-profile/sdwan/sig-security/{sigSecurityId}/sig/{sigSecurityProfileParcelId}
        if self._request_adapter.param_checker(
            [(sig_security_id, str), (sig_security_profile_parcel_id, str)], []
        ):
            params = {
                "sigSecurityId": sig_security_id,
                "sigSecurityProfileParcelId": sig_security_profile_parcel_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/sig-security/{sigSecurityId}/sig/{sigSecurityProfileParcelId}",
                return_type=GetSingleSdwanSigSecuritySigPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/sig-security/{sigSecurityId}/sig
        if self._request_adapter.param_checker(
            [(sig_security_id, str)], [sig_security_profile_parcel_id]
        ):
            params = {
                "sigSecurityId": sig_security_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/sig-security/{sigSecurityId}/sig",
                return_type=GetListSdwanSigSecuritySigPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
