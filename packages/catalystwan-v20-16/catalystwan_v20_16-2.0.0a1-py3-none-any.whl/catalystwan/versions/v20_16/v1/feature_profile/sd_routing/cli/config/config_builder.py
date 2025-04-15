# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingCliAddOnFeaturePostRequest,
    CreateSdroutingCliAddOnFeaturePostResponse,
    EditSdroutingCliAddOnFeaturePutRequest,
    EditSdroutingCliAddOnFeaturePutResponse,
    GetListSdRoutingCliConfigPayload,
    GetSingleSdRoutingCliConfigPayload,
)


class ConfigBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/cli/{cliId}/config
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, cli_id: str, payload: CreateSdroutingCliAddOnFeaturePostRequest, **kw
    ) -> CreateSdroutingCliAddOnFeaturePostResponse:
        """
        Create a SD-Routing CLI Add-On Feature for CLI Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/cli/{cliId}/config

        :param cli_id: Cli Profile ID
        :param payload: SD-Routing CLI Add-On Feature for CLI Feature Profile
        :returns: CreateSdroutingCliAddOnFeaturePostResponse
        """
        params = {
            "cliId": cli_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/cli/{cliId}/config",
            return_type=CreateSdroutingCliAddOnFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self, cli_id: str, config_id: str, payload: EditSdroutingCliAddOnFeaturePutRequest, **kw
    ) -> EditSdroutingCliAddOnFeaturePutResponse:
        """
        Edit a SD-Routing CLI Add-On Feature for CLI Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/cli/{cliId}/config/{configId}

        :param cli_id: Cli Profile ID
        :param config_id: Config Feature ID
        :param payload: SD-Routing CLI Add-On Feature for CLI Feature Profile
        :returns: EditSdroutingCliAddOnFeaturePutResponse
        """
        params = {
            "cliId": cli_id,
            "configId": config_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/cli/{cliId}/config/{configId}",
            return_type=EditSdroutingCliAddOnFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, cli_id: str, config_id: str, **kw):
        """
        Delete a SD-Routing CLI Add-On Feature for CLI Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/cli/{cliId}/config/{configId}

        :param cli_id: Cli Profile ID
        :param config_id: Config Feature ID
        :returns: None
        """
        params = {
            "cliId": cli_id,
            "configId": config_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/cli/{cliId}/config/{configId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, cli_id: str, config_id: str, **kw) -> GetSingleSdRoutingCliConfigPayload:
        """
        Get a SD-Routing CLI Add-On Feature for CLI Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/cli/{cliId}/config/{configId}

        :param cli_id: Cli Profile ID
        :param config_id: Config Feature ID
        :returns: GetSingleSdRoutingCliConfigPayload
        """
        ...

    @overload
    def get(self, cli_id: str, **kw) -> GetListSdRoutingCliConfigPayload:
        """
        Get all SD-Routing CLI Add-On Features for CLI Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/cli/{cliId}/config

        :param cli_id: Cli Profile ID
        :returns: GetListSdRoutingCliConfigPayload
        """
        ...

    def get(
        self, cli_id: str, config_id: Optional[str] = None, **kw
    ) -> Union[GetListSdRoutingCliConfigPayload, GetSingleSdRoutingCliConfigPayload]:
        # /dataservice/v1/feature-profile/sd-routing/cli/{cliId}/config/{configId}
        if self._request_adapter.param_checker([(cli_id, str), (config_id, str)], []):
            params = {
                "cliId": cli_id,
                "configId": config_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/cli/{cliId}/config/{configId}",
                return_type=GetSingleSdRoutingCliConfigPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/cli/{cliId}/config
        if self._request_adapter.param_checker([(cli_id, str)], [config_id]):
            params = {
                "cliId": cli_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/cli/{cliId}/config",
                return_type=GetListSdRoutingCliConfigPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
