# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateBasicProfileFeatureForSystemPostRequest,
    CreateBasicProfileFeatureForSystemPostResponse,
    EditBasicProfileFeatureForSystemPutRequest,
    EditBasicProfileFeatureForSystemPutResponse,
    GetListSdwanSystemBasicPayload,
    GetSingleSdwanSystemBasicPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class BasicBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/system/basic
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateBasicProfileFeatureForSystemPostRequest, **kw
    ) -> CreateBasicProfileFeatureForSystemPostResponse:
        """
        Create a Basic Profile Feature for System feature profile
        POST /dataservice/v1/feature-profile/sdwan/system/{systemId}/basic

        :param system_id: Feature Profile ID
        :param payload: Basic Profile Feature
        :returns: CreateBasicProfileFeatureForSystemPostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/basic",
            return_type=CreateBasicProfileFeatureForSystemPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        system_id: str,
        basic_id: str,
        payload: EditBasicProfileFeatureForSystemPutRequest,
        **kw,
    ) -> EditBasicProfileFeatureForSystemPutResponse:
        """
        Update a Basic Profile Feature for System feature profile
        PUT /dataservice/v1/feature-profile/sdwan/system/{systemId}/basic/{basicId}

        :param system_id: Feature Profile ID
        :param basic_id: Profile Feature ID
        :param payload: Basic Profile Feature
        :returns: EditBasicProfileFeatureForSystemPutResponse
        """
        params = {
            "systemId": system_id,
            "basicId": basic_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/basic/{basicId}",
            return_type=EditBasicProfileFeatureForSystemPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, basic_id: str, **kw):
        """
        Delete a Basic Profile Feature for System feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/system/{systemId}/basic/{basicId}

        :param system_id: Feature Profile ID
        :param basic_id: Profile Feature ID
        :returns: None
        """
        params = {
            "systemId": system_id,
            "basicId": basic_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/basic/{basicId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, system_id: str, basic_id: str, **kw) -> GetSingleSdwanSystemBasicPayload:
        """
        Get Basic Profile Feature by FeatureId for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/basic/{basicId}

        :param system_id: Feature Profile ID
        :param basic_id: Profile Feature ID
        :returns: GetSingleSdwanSystemBasicPayload
        """
        ...

    @overload
    def get(self, system_id: str, **kw) -> GetListSdwanSystemBasicPayload:
        """
        Get Basic Profile Feature for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/basic

        :param system_id: Feature Profile ID
        :returns: GetListSdwanSystemBasicPayload
        """
        ...

    def get(
        self, system_id: str, basic_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanSystemBasicPayload, GetSingleSdwanSystemBasicPayload]:
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/basic/{basicId}
        if self._request_adapter.param_checker([(system_id, str), (basic_id, str)], []):
            params = {
                "systemId": system_id,
                "basicId": basic_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/basic/{basicId}",
                return_type=GetSingleSdwanSystemBasicPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/basic
        if self._request_adapter.param_checker([(system_id, str)], [basic_id]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/basic",
                return_type=GetListSdwanSystemBasicPayload,
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
