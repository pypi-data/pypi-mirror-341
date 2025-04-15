# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingGlobalSettingFeaturePostRequest,
    CreateSdroutingGlobalSettingFeaturePostResponse,
    EditSdroutingGlobalSettingFeaturePutRequest,
    EditSdroutingGlobalSettingFeaturePutResponse,
    GetListSdRoutingSystemGlobalPayload,
    GetSingleSdRoutingSystemGlobalPayload,
)


class GlobalBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/system/{systemId}/global
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateSdroutingGlobalSettingFeaturePostRequest, **kw
    ) -> CreateSdroutingGlobalSettingFeaturePostResponse:
        """
        Create a SD-Routing global setting feature from a specific system feature profile
        POST /dataservice/v1/feature-profile/sd-routing/system/{systemId}/global

        :param system_id: System Profile ID
        :param payload: SD-Routing global setting feature from a specific system feature profile
        :returns: CreateSdroutingGlobalSettingFeaturePostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/global",
            return_type=CreateSdroutingGlobalSettingFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        system_id: str,
        global_id: str,
        payload: EditSdroutingGlobalSettingFeaturePutRequest,
        **kw,
    ) -> EditSdroutingGlobalSettingFeaturePutResponse:
        """
        Edit the SD-Routing global setting feature from a specific system feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/system/{systemId}/global/{globalId}

        :param system_id: System Profile ID
        :param global_id: Global Setting Feature ID
        :param payload: SD-Routing global setting feature from a specific system feature profile
        :returns: EditSdroutingGlobalSettingFeaturePutResponse
        """
        params = {
            "systemId": system_id,
            "globalId": global_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/global/{globalId}",
            return_type=EditSdroutingGlobalSettingFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, global_id: str, **kw):
        """
        Delete the SD-Routing global setting feature from a specific system feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/system/{systemId}/global/{globalId}

        :param system_id: System Profile ID
        :param global_id: Global Setting Feature ID
        :returns: None
        """
        params = {
            "systemId": system_id,
            "globalId": global_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/global/{globalId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, system_id: str, global_id: str, **kw) -> GetSingleSdRoutingSystemGlobalPayload:
        """
        Get the SD-Routing global setting feature from a specific system feature profile
        GET /dataservice/v1/feature-profile/sd-routing/system/{systemId}/global/{globalId}

        :param system_id: System Profile ID
        :param global_id: Global Setting Feature ID
        :returns: GetSingleSdRoutingSystemGlobalPayload
        """
        ...

    @overload
    def get(self, system_id: str, **kw) -> GetListSdRoutingSystemGlobalPayload:
        """
        Get all SD-Routing global setting features from a specific system feature profile
        GET /dataservice/v1/feature-profile/sd-routing/system/{systemId}/global

        :param system_id: System Profile ID
        :returns: GetListSdRoutingSystemGlobalPayload
        """
        ...

    def get(
        self, system_id: str, global_id: Optional[str] = None, **kw
    ) -> Union[GetListSdRoutingSystemGlobalPayload, GetSingleSdRoutingSystemGlobalPayload]:
        # /dataservice/v1/feature-profile/sd-routing/system/{systemId}/global/{globalId}
        if self._request_adapter.param_checker([(system_id, str), (global_id, str)], []):
            params = {
                "systemId": system_id,
                "globalId": global_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/global/{globalId}",
                return_type=GetSingleSdRoutingSystemGlobalPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/system/{systemId}/global
        if self._request_adapter.param_checker([(system_id, str)], [global_id]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/global",
                return_type=GetListSdRoutingSystemGlobalPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
