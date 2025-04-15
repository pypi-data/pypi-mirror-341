# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdwanOtherFeatureProfilePostRequest,
    CreateSdwanOtherFeatureProfilePostResponse,
    EditSdwanOtherFeatureProfilePutRequest,
    EditSdwanOtherFeatureProfilePutResponse,
    GetSdwanOtherFeatureProfilesGetResponse,
    GetSingleSdwanOtherPayload,
)

if TYPE_CHECKING:
    from .thousandeyes.thousandeyes_builder import ThousandeyesBuilder
    from .ucse.ucse_builder import UcseBuilder


class OtherBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/other
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, payload: CreateSdwanOtherFeatureProfilePostRequest, **kw
    ) -> CreateSdwanOtherFeatureProfilePostResponse:
        """
        Create a SDWAN Other Feature Profile
        POST /dataservice/v1/feature-profile/sdwan/other

        :param payload: SDWAN Feature profile
        :returns: CreateSdwanOtherFeatureProfilePostResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/other",
            return_type=CreateSdwanOtherFeatureProfilePostResponse,
            payload=payload,
            **kw,
        )

    def put(
        self, other_id: str, payload: EditSdwanOtherFeatureProfilePutRequest, **kw
    ) -> EditSdwanOtherFeatureProfilePutResponse:
        """
        Edit a SDWAN Other Feature Profile
        PUT /dataservice/v1/feature-profile/sdwan/other/{otherId}

        :param other_id: Feature Profile Id
        :param payload: SDWAN Feature profile
        :returns: EditSdwanOtherFeatureProfilePutResponse
        """
        params = {
            "otherId": other_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/other/{otherId}",
            return_type=EditSdwanOtherFeatureProfilePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, other_id: str, **kw):
        """
        Delete Feature Profile
        DELETE /dataservice/v1/feature-profile/sdwan/other/{otherId}

        :param other_id: Other id
        :returns: None
        """
        params = {
            "otherId": other_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/v1/feature-profile/sdwan/other/{otherId}", params=params, **kw
        )

    @overload
    def get(self, *, other_id: str, **kw) -> GetSingleSdwanOtherPayload:
        """
        Get a SDWAN Other Feature Profile with otherId
        GET /dataservice/v1/feature-profile/sdwan/other/{otherId}

        :param other_id: Feature Profile Id
        :returns: GetSingleSdwanOtherPayload
        """
        ...

    @overload
    def get(
        self, *, offset: Optional[int] = None, limit: Optional[int] = 0, **kw
    ) -> List[GetSdwanOtherFeatureProfilesGetResponse]:
        """
        Get all SDWAN Feature Profiles with giving Family and profile type
        GET /dataservice/v1/feature-profile/sdwan/other

        :param offset: Pagination offset
        :param limit: Pagination limit
        :returns: List[GetSdwanOtherFeatureProfilesGetResponse]
        """
        ...

    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        other_id: Optional[str] = None,
        **kw,
    ) -> Union[List[GetSdwanOtherFeatureProfilesGetResponse], GetSingleSdwanOtherPayload]:
        # /dataservice/v1/feature-profile/sdwan/other/{otherId}
        if self._request_adapter.param_checker([(other_id, str)], [offset, limit]):
            params = {
                "otherId": other_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/other/{otherId}",
                return_type=GetSingleSdwanOtherPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/other
        if self._request_adapter.param_checker([], [other_id]):
            params = {
                "offset": offset,
                "limit": limit,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/other",
                return_type=List[GetSdwanOtherFeatureProfilesGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def thousandeyes(self) -> ThousandeyesBuilder:
        """
        The thousandeyes property
        """
        from .thousandeyes.thousandeyes_builder import ThousandeyesBuilder

        return ThousandeyesBuilder(self._request_adapter)

    @property
    def ucse(self) -> UcseBuilder:
        """
        The ucse property
        """
        from .ucse.ucse_builder import UcseBuilder

        return UcseBuilder(self._request_adapter)
