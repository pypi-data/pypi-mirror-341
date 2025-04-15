# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingFlexiblePortSpeedFeaturePostRequest,
    CreateSdroutingFlexiblePortSpeedFeaturePostResponse,
    EditSdroutingFlexiblePortSpeedFeaturePutRequest,
    EditSdroutingFlexiblePortSpeedFeaturePutResponse,
    GetListSdRoutingSystemFlexiblePortSpeedPayload,
    GetSingleSdRoutingSystemFlexiblePortSpeedPayload,
)


class FlexiblePortSpeedBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/system/{systemId}/flexible-port-speed
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateSdroutingFlexiblePortSpeedFeaturePostRequest, **kw
    ) -> CreateSdroutingFlexiblePortSpeedFeaturePostResponse:
        """
        Create a SD-Routing flexible port speed feature from a specific system feature profile
        POST /dataservice/v1/feature-profile/sd-routing/system/{systemId}/flexible-port-speed

        :param system_id: System Profile ID
        :param payload: SD-Routing flexible port speed feature from a specific system feature profile
        :returns: CreateSdroutingFlexiblePortSpeedFeaturePostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/flexible-port-speed",
            return_type=CreateSdroutingFlexiblePortSpeedFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        system_id: str,
        flexible_port_speed_id: str,
        payload: EditSdroutingFlexiblePortSpeedFeaturePutRequest,
        **kw,
    ) -> EditSdroutingFlexiblePortSpeedFeaturePutResponse:
        """
        Edit the SD-Routing flexible port speed feature from a specific system feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/system/{systemId}/flexible-port-speed/{flexiblePortSpeedId}

        :param system_id: System Profile ID
        :param flexible_port_speed_id: Flexible Port Speed Feature ID
        :param payload: SD-Routing flexible port speed feature from a specific system feature profile
        :returns: EditSdroutingFlexiblePortSpeedFeaturePutResponse
        """
        params = {
            "systemId": system_id,
            "flexiblePortSpeedId": flexible_port_speed_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/flexible-port-speed/{flexiblePortSpeedId}",
            return_type=EditSdroutingFlexiblePortSpeedFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, flexible_port_speed_id: str, **kw):
        """
        Delete the SD-Routing flexible port speed feature from a specific system feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/system/{systemId}/flexible-port-speed/{flexiblePortSpeedId}

        :param system_id: System Profile ID
        :param flexible_port_speed_id: Flexible Port Speed Feature ID
        :returns: None
        """
        params = {
            "systemId": system_id,
            "flexiblePortSpeedId": flexible_port_speed_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/flexible-port-speed/{flexiblePortSpeedId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, system_id: str, flexible_port_speed_id: str, **kw
    ) -> GetSingleSdRoutingSystemFlexiblePortSpeedPayload:
        """
        Get the SD-Routing flexible port speed feature from a specific system feature profile
        GET /dataservice/v1/feature-profile/sd-routing/system/{systemId}/flexible-port-speed/{flexiblePortSpeedId}

        :param system_id: System Profile ID
        :param flexible_port_speed_id: Flexible Port Speed Feature ID
        :returns: GetSingleSdRoutingSystemFlexiblePortSpeedPayload
        """
        ...

    @overload
    def get(self, system_id: str, **kw) -> GetListSdRoutingSystemFlexiblePortSpeedPayload:
        """
        Get all SD-Routing flexible port speed features from a specific system feature profile
        GET /dataservice/v1/feature-profile/sd-routing/system/{systemId}/flexible-port-speed

        :param system_id: System Profile ID
        :returns: GetListSdRoutingSystemFlexiblePortSpeedPayload
        """
        ...

    def get(
        self, system_id: str, flexible_port_speed_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingSystemFlexiblePortSpeedPayload,
        GetSingleSdRoutingSystemFlexiblePortSpeedPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/system/{systemId}/flexible-port-speed/{flexiblePortSpeedId}
        if self._request_adapter.param_checker(
            [(system_id, str), (flexible_port_speed_id, str)], []
        ):
            params = {
                "systemId": system_id,
                "flexiblePortSpeedId": flexible_port_speed_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/flexible-port-speed/{flexiblePortSpeedId}",
                return_type=GetSingleSdRoutingSystemFlexiblePortSpeedPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/system/{systemId}/flexible-port-speed
        if self._request_adapter.param_checker([(system_id, str)], [flexible_port_speed_id]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/flexible-port-speed",
                return_type=GetListSdRoutingSystemFlexiblePortSpeedPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
