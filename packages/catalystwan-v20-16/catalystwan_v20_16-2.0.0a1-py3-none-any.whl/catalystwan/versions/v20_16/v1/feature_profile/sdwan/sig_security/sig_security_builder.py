# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdwanSigSecurityFeatureProfilePostRequest,
    CreateSdwanSigSecurityFeatureProfilePostResponse,
    EditSdwanSigSecurityFeatureProfilePutRequest,
    EditSdwanSigSecurityFeatureProfilePutResponse,
    GetSdwanSigSecurityFeatureProfilesGetResponse,
    GetSingleSdwanSigSecurityPayload,
)

if TYPE_CHECKING:
    from .sig.sig_builder import SigBuilder


class SigSecurityBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/sig-security
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, payload: CreateSdwanSigSecurityFeatureProfilePostRequest, **kw
    ) -> CreateSdwanSigSecurityFeatureProfilePostResponse:
        """
        Create a SDWAN Sig Security Feature Profile
        POST /dataservice/v1/feature-profile/sdwan/sig-security

        :param payload: SDWAN Feature profile
        :returns: CreateSdwanSigSecurityFeatureProfilePostResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/sig-security",
            return_type=CreateSdwanSigSecurityFeatureProfilePostResponse,
            payload=payload,
            **kw,
        )

    def put(
        self, sig_security_id: str, payload: EditSdwanSigSecurityFeatureProfilePutRequest, **kw
    ) -> EditSdwanSigSecurityFeatureProfilePutResponse:
        """
        Edit a SDWAN Sig Security Feature Profile
        PUT /dataservice/v1/feature-profile/sdwan/sig-security/{sigSecurityId}

        :param sig_security_id: Feature Profile Id
        :param payload: SDWAN Feature profile
        :returns: EditSdwanSigSecurityFeatureProfilePutResponse
        """
        params = {
            "sigSecurityId": sig_security_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/sig-security/{sigSecurityId}",
            return_type=EditSdwanSigSecurityFeatureProfilePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, sig_security_id: str, **kw):
        """
        Delete Feature Profile
        DELETE /dataservice/v1/feature-profile/sdwan/sig-security/{sigSecurityId}

        :param sig_security_id: Sig security id
        :returns: None
        """
        params = {
            "sigSecurityId": sig_security_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/sig-security/{sigSecurityId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, *, sig_security_id: str, references: Optional[bool] = False, **kw
    ) -> GetSingleSdwanSigSecurityPayload:
        """
        Get a SDWAN Sig Security Feature Profile with sigSecurityId
        GET /dataservice/v1/feature-profile/sdwan/sig-security/{sigSecurityId}

        :param sig_security_id: Feature Profile Id
        :param references: get associated group details
        :returns: GetSingleSdwanSigSecurityPayload
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
    ) -> List[GetSdwanSigSecurityFeatureProfilesGetResponse]:
        """
        Get all SDWAN Feature Profiles with giving Family and profile type
        GET /dataservice/v1/feature-profile/sdwan/sig-security

        :param offset: Pagination offset
        :param limit: Pagination limit
        :param reference_count: get associated group details
        :returns: List[GetSdwanSigSecurityFeatureProfilesGetResponse]
        """
        ...

    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        reference_count: Optional[bool] = None,
        sig_security_id: Optional[str] = None,
        references: Optional[bool] = None,
        **kw,
    ) -> Union[
        List[GetSdwanSigSecurityFeatureProfilesGetResponse], GetSingleSdwanSigSecurityPayload
    ]:
        # /dataservice/v1/feature-profile/sdwan/sig-security/{sigSecurityId}
        if self._request_adapter.param_checker(
            [(sig_security_id, str)], [offset, limit, reference_count]
        ):
            params = {
                "sigSecurityId": sig_security_id,
                "references": references,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/sig-security/{sigSecurityId}",
                return_type=GetSingleSdwanSigSecurityPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/sig-security
        if self._request_adapter.param_checker([], [sig_security_id, references]):
            params = {
                "offset": offset,
                "limit": limit,
                "referenceCount": reference_count,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/sig-security",
                return_type=List[GetSdwanSigSecurityFeatureProfilesGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def sig(self) -> SigBuilder:
        """
        The sig property
        """
        from .sig.sig_builder import SigBuilder

        return SigBuilder(self._request_adapter)
