# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSigSecurityProfileParcelPostRequest1,
    CreateSigSecurityProfileParcelPostRequest2,
    CreateSigSecurityProfileParcelPostResponse,
    EditSigSecurityProfileParcelPutRequest1,
    EditSigSecurityProfileParcelPutRequest2,
    EditSigSecurityProfileParcelPutResponse,
    GetListSdwanDnsSecurityDnsPayload,
    GetSingleSdwanDnsSecurityDnsPayload,
)


class DnsBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/dns-security/{dnsSecurityId}/dns
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        dns_security_id: str,
        payload: Union[
            CreateSigSecurityProfileParcelPostRequest1, CreateSigSecurityProfileParcelPostRequest2
        ],
        **kw,
    ) -> CreateSigSecurityProfileParcelPostResponse:
        """
        Create Parcel for Sig Security Policy
        POST /dataservice/v1/feature-profile/sdwan/dns-security/{dnsSecurityId}/dns

        :param dns_security_id: Feature Profile ID
        :param payload: Sig Security Profile Parcel
        :returns: CreateSigSecurityProfileParcelPostResponse
        """
        params = {
            "dnsSecurityId": dns_security_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/dns-security/{dnsSecurityId}/dns",
            return_type=CreateSigSecurityProfileParcelPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        dns_security_id: str,
        dns_security_profile_parcel_id: str,
        payload: Union[
            EditSigSecurityProfileParcelPutRequest1, EditSigSecurityProfileParcelPutRequest2
        ],
        **kw,
    ) -> EditSigSecurityProfileParcelPutResponse:
        """
        Update a Sig Security Profile Parcel
        PUT /dataservice/v1/feature-profile/sdwan/dns-security/{dnsSecurityId}/dns/{dnsSecurityProfileParcelId}

        :param dns_security_id: Feature Profile ID
        :param dns_security_profile_parcel_id: Profile Parcel ID
        :param payload: Sig Security Profile Parcel
        :returns: EditSigSecurityProfileParcelPutResponse
        """
        params = {
            "dnsSecurityId": dns_security_id,
            "dnsSecurityProfileParcelId": dns_security_profile_parcel_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/dns-security/{dnsSecurityId}/dns/{dnsSecurityProfileParcelId}",
            return_type=EditSigSecurityProfileParcelPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, dns_security_id: str, dns_security_profile_parcel_id: str, **kw):
        """
        Delete a SigSecurity Profile Parcel
        DELETE /dataservice/v1/feature-profile/sdwan/dns-security/{dnsSecurityId}/dns/{dnsSecurityProfileParcelId}

        :param dns_security_id: Feature Profile ID
        :param dns_security_profile_parcel_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "dnsSecurityId": dns_security_id,
            "dnsSecurityProfileParcelId": dns_security_profile_parcel_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/dns-security/{dnsSecurityId}/dns/{dnsSecurityProfileParcelId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, dns_security_id: str, dns_security_profile_parcel_id: str, **kw
    ) -> GetSingleSdwanDnsSecurityDnsPayload:
        """
        Get SigSecurity Profile Parcel by parcelId
        GET /dataservice/v1/feature-profile/sdwan/dns-security/{dnsSecurityId}/dns/{dnsSecurityProfileParcelId}

        :param dns_security_id: Feature Profile ID
        :param dns_security_profile_parcel_id: Profile Parcel ID
        :returns: GetSingleSdwanDnsSecurityDnsPayload
        """
        ...

    @overload
    def get(self, dns_security_id: str, **kw) -> GetListSdwanDnsSecurityDnsPayload:
        """
        Get Sig Security Profile Parcels for a given ParcelType
        GET /dataservice/v1/feature-profile/sdwan/dns-security/{dnsSecurityId}/dns

        :param dns_security_id: Feature Profile ID
        :returns: GetListSdwanDnsSecurityDnsPayload
        """
        ...

    def get(
        self, dns_security_id: str, dns_security_profile_parcel_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanDnsSecurityDnsPayload, GetSingleSdwanDnsSecurityDnsPayload]:
        # /dataservice/v1/feature-profile/sdwan/dns-security/{dnsSecurityId}/dns/{dnsSecurityProfileParcelId}
        if self._request_adapter.param_checker(
            [(dns_security_id, str), (dns_security_profile_parcel_id, str)], []
        ):
            params = {
                "dnsSecurityId": dns_security_id,
                "dnsSecurityProfileParcelId": dns_security_profile_parcel_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/dns-security/{dnsSecurityId}/dns/{dnsSecurityProfileParcelId}",
                return_type=GetSingleSdwanDnsSecurityDnsPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/dns-security/{dnsSecurityId}/dns
        if self._request_adapter.param_checker(
            [(dns_security_id, str)], [dns_security_profile_parcel_id]
        ):
            params = {
                "dnsSecurityId": dns_security_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/dns-security/{dnsSecurityId}/dns",
                return_type=GetListSdwanDnsSecurityDnsPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
