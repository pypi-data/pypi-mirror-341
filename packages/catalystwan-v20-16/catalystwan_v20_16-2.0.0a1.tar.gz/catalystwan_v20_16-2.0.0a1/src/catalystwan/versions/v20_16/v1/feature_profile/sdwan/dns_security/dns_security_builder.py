# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdwanDnsSecurityFeatureProfilePostRequest,
    CreateSdwanDnsSecurityFeatureProfilePostResponse,
    EditSdwanDnsSecurityFeatureProfilePutRequest,
    EditSdwanDnsSecurityFeatureProfilePutResponse,
    GetSdwanDnsSecurityFeatureProfilesGetResponse,
    GetSingleSdwanDnsSecurityPayload,
)

if TYPE_CHECKING:
    from .dns.dns_builder import DnsBuilder


class DnsSecurityBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/dns-security
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, payload: CreateSdwanDnsSecurityFeatureProfilePostRequest, **kw
    ) -> CreateSdwanDnsSecurityFeatureProfilePostResponse:
        """
        Create a SDWAN Dns Security Feature Profile
        POST /dataservice/v1/feature-profile/sdwan/dns-security

        :param payload: SDWAN Feature profile
        :returns: CreateSdwanDnsSecurityFeatureProfilePostResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/dns-security",
            return_type=CreateSdwanDnsSecurityFeatureProfilePostResponse,
            payload=payload,
            **kw,
        )

    def put(
        self, dns_security_id: str, payload: EditSdwanDnsSecurityFeatureProfilePutRequest, **kw
    ) -> EditSdwanDnsSecurityFeatureProfilePutResponse:
        """
        Edit a SDWAN Dns Security Feature Profile
        PUT /dataservice/v1/feature-profile/sdwan/dns-security/{dnsSecurityId}

        :param dns_security_id: Feature Profile Id
        :param payload: SDWAN Feature profile
        :returns: EditSdwanDnsSecurityFeatureProfilePutResponse
        """
        params = {
            "dnsSecurityId": dns_security_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/dns-security/{dnsSecurityId}",
            return_type=EditSdwanDnsSecurityFeatureProfilePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, dns_security_id: str, **kw):
        """
        Delete Feature Profile
        DELETE /dataservice/v1/feature-profile/sdwan/dns-security/{dnsSecurityId}

        :param dns_security_id: Dns security id
        :returns: None
        """
        params = {
            "dnsSecurityId": dns_security_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/dns-security/{dnsSecurityId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, *, dns_security_id: str, references: Optional[bool] = False, **kw
    ) -> GetSingleSdwanDnsSecurityPayload:
        """
        Get a SDWAN Dns Security Feature Profile with dnsSecurityId
        GET /dataservice/v1/feature-profile/sdwan/dns-security/{dnsSecurityId}

        :param dns_security_id: Feature Profile Id
        :param references: get associated group details
        :returns: GetSingleSdwanDnsSecurityPayload
        """
        ...

    @overload
    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = 0,
        reference_count: Optional[bool] = False,
        **kw,
    ) -> List[GetSdwanDnsSecurityFeatureProfilesGetResponse]:
        """
        Get all SDWAN Feature Profiles with giving Family and profile type
        GET /dataservice/v1/feature-profile/sdwan/dns-security

        :param offset: Pagination offset
        :param limit: Pagination limit
        :param reference_count: get associated group details
        :returns: List[GetSdwanDnsSecurityFeatureProfilesGetResponse]
        """
        ...

    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        reference_count: Optional[bool] = None,
        dns_security_id: Optional[str] = None,
        references: Optional[bool] = None,
        **kw,
    ) -> Union[
        List[GetSdwanDnsSecurityFeatureProfilesGetResponse], GetSingleSdwanDnsSecurityPayload
    ]:
        # /dataservice/v1/feature-profile/sdwan/dns-security/{dnsSecurityId}
        if self._request_adapter.param_checker(
            [(dns_security_id, str)], [offset, limit, reference_count]
        ):
            params = {
                "dnsSecurityId": dns_security_id,
                "references": references,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/dns-security/{dnsSecurityId}",
                return_type=GetSingleSdwanDnsSecurityPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/dns-security
        if self._request_adapter.param_checker([], [dns_security_id, references]):
            params = {
                "offset": offset,
                "limit": limit,
                "referenceCount": reference_count,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/dns-security",
                return_type=List[GetSdwanDnsSecurityFeatureProfilesGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def dns(self) -> DnsBuilder:
        """
        The dns property
        """
        from .dns.dns_builder import DnsBuilder

        return DnsBuilder(self._request_adapter)
