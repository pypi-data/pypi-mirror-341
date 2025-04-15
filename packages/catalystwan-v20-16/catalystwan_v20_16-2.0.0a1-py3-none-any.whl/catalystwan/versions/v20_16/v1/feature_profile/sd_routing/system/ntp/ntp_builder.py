# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingNtpFeaturePostRequest,
    CreateSdroutingNtpFeaturePostResponse,
    EditSdroutingNtpFeaturePutRequest,
    EditSdroutingNtpFeaturePutResponse,
    GetListSdRoutingSystemNtpSdRoutingPayload,
    GetSingleSdRoutingSystemNtpSdRoutingPayload,
)


class NtpBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/system/{systemId}/ntp
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateSdroutingNtpFeaturePostRequest, **kw
    ) -> CreateSdroutingNtpFeaturePostResponse:
        """
        Create a SD-Routing NTP feature from a specific system feature profile
        POST /dataservice/v1/feature-profile/sd-routing/system/{systemId}/ntp

        :param system_id: System Profile ID
        :param payload: SD-Routing NTP feature from a specific system feature profile
        :returns: CreateSdroutingNtpFeaturePostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/ntp",
            return_type=CreateSdroutingNtpFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self, system_id: str, ntp_id: str, payload: EditSdroutingNtpFeaturePutRequest, **kw
    ) -> EditSdroutingNtpFeaturePutResponse:
        """
        Edit the SD-Routing NTP feature from a specific system feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/system/{systemId}/ntp/{ntpId}

        :param system_id: System Profile ID
        :param ntp_id: NTP Feature ID
        :param payload: SD-Routing NTP feature from a specific system feature profile
        :returns: EditSdroutingNtpFeaturePutResponse
        """
        params = {
            "systemId": system_id,
            "ntpId": ntp_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/ntp/{ntpId}",
            return_type=EditSdroutingNtpFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, ntp_id: str, **kw):
        """
        Delete the SD-Routing NTP feature from a specific system feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/system/{systemId}/ntp/{ntpId}

        :param system_id: System Profile ID
        :param ntp_id: NTP Feature ID
        :returns: None
        """
        params = {
            "systemId": system_id,
            "ntpId": ntp_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/ntp/{ntpId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, system_id: str, ntp_id: str, **kw) -> GetSingleSdRoutingSystemNtpSdRoutingPayload:
        """
        Get the SD-Routing NTP feature from a specific system feature profile
        GET /dataservice/v1/feature-profile/sd-routing/system/{systemId}/ntp/{ntpId}

        :param system_id: System Profile ID
        :param ntp_id: NTP Feature ID
        :returns: GetSingleSdRoutingSystemNtpSdRoutingPayload
        """
        ...

    @overload
    def get(self, system_id: str, **kw) -> GetListSdRoutingSystemNtpSdRoutingPayload:
        """
        Get all SD-Routing NTP features from a specific system feature profile
        GET /dataservice/v1/feature-profile/sd-routing/system/{systemId}/ntp

        :param system_id: System Profile ID
        :returns: GetListSdRoutingSystemNtpSdRoutingPayload
        """
        ...

    def get(
        self, system_id: str, ntp_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingSystemNtpSdRoutingPayload, GetSingleSdRoutingSystemNtpSdRoutingPayload
    ]:
        # /dataservice/v1/feature-profile/sd-routing/system/{systemId}/ntp/{ntpId}
        if self._request_adapter.param_checker([(system_id, str), (ntp_id, str)], []):
            params = {
                "systemId": system_id,
                "ntpId": ntp_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/ntp/{ntpId}",
                return_type=GetSingleSdRoutingSystemNtpSdRoutingPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/system/{systemId}/ntp
        if self._request_adapter.param_checker([(system_id, str)], [ntp_id]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/ntp",
                return_type=GetListSdRoutingSystemNtpSdRoutingPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
