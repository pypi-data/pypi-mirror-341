# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingIosClassicCliAddOnFeaturePostRequest,
    CreateSdroutingIosClassicCliAddOnFeaturePostResponse,
    EditSdroutingIosClassicCliAddOnFeaturePutRequest,
    EditSdroutingIosClassicCliAddOnFeaturePutResponse,
    GetListSdRoutingCliIosConfigPayload,
    GetSingleSdRoutingCliIosConfigPayload,
)


class IosConfigBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/cli/{cliId}/ios-config
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, cli_id: str, payload: CreateSdroutingIosClassicCliAddOnFeaturePostRequest, **kw
    ) -> CreateSdroutingIosClassicCliAddOnFeaturePostResponse:
        """
        SD-Routing Ios Classic CLI Add-On Feature for CLI Feature Profile for POST requests
        POST /dataservice/v1/feature-profile/sd-routing/cli/{cliId}/ios-config

        :param cli_id: Feature Profile ID
        :param payload: SD-Routing Ios Classic CLI Add-On Feature for CLI Feature Profile
        :returns: CreateSdroutingIosClassicCliAddOnFeaturePostResponse
        """
        params = {
            "cliId": cli_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/cli/{cliId}/ios-config",
            return_type=CreateSdroutingIosClassicCliAddOnFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        cli_id: str,
        ios_config_id: str,
        payload: EditSdroutingIosClassicCliAddOnFeaturePutRequest,
        **kw,
    ) -> EditSdroutingIosClassicCliAddOnFeaturePutResponse:
        """
        SD-Routing Ios Classic CLI Add-On Feature for CLI Feature Profile for PUT requests
        PUT /dataservice/v1/feature-profile/sd-routing/cli/{cliId}/ios-config/{iosConfigId}

        :param cli_id: Feature Profile ID
        :param ios_config_id: Ios Config ID
        :param payload: SD-Routing Ios Classic CLI Add-On Feature for CLI Feature Profile
        :returns: EditSdroutingIosClassicCliAddOnFeaturePutResponse
        """
        params = {
            "cliId": cli_id,
            "iosConfigId": ios_config_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/cli/{cliId}/ios-config/{iosConfigId}",
            return_type=EditSdroutingIosClassicCliAddOnFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, cli_id: str, ios_config_id: str, **kw):
        """
        Delete a SD-Routing Ios Classic CLI Add-On Feature for CLI Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/cli/{cliId}/ios-config/{iosConfigId}

        :param cli_id: Feature Profile ID
        :param ios_config_id: Ios Config ID
        :returns: None
        """
        params = {
            "cliId": cli_id,
            "iosConfigId": ios_config_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/cli/{cliId}/ios-config/{iosConfigId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, cli_id: str, ios_config_id: str, **kw) -> GetSingleSdRoutingCliIosConfigPayload:
        """
        SD-Routing Ios Classic CLI Add-On Feature for CLI Feature Profile for GET requests
        GET /dataservice/v1/feature-profile/sd-routing/cli/{cliId}/ios-config/{iosConfigId}

        :param cli_id: Feature Profile ID
        :param ios_config_id: Ios Config ID
        :returns: GetSingleSdRoutingCliIosConfigPayload
        """
        ...

    @overload
    def get(self, cli_id: str, **kw) -> GetListSdRoutingCliIosConfigPayload:
        """
        SD-Routing Ios Classic CLI Add-On Features for CLI Feature Profile for GET requests
        GET /dataservice/v1/feature-profile/sd-routing/cli/{cliId}/ios-config

        :param cli_id: Feature Profile ID
        :returns: GetListSdRoutingCliIosConfigPayload
        """
        ...

    def get(
        self, cli_id: str, ios_config_id: Optional[str] = None, **kw
    ) -> Union[GetListSdRoutingCliIosConfigPayload, GetSingleSdRoutingCliIosConfigPayload]:
        # /dataservice/v1/feature-profile/sd-routing/cli/{cliId}/ios-config/{iosConfigId}
        if self._request_adapter.param_checker([(cli_id, str), (ios_config_id, str)], []):
            params = {
                "cliId": cli_id,
                "iosConfigId": ios_config_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/cli/{cliId}/ios-config/{iosConfigId}",
                return_type=GetSingleSdRoutingCliIosConfigPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/cli/{cliId}/ios-config
        if self._request_adapter.param_checker([(cli_id, str)], [ios_config_id]):
            params = {
                "cliId": cli_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/cli/{cliId}/ios-config",
                return_type=GetListSdRoutingCliIosConfigPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
