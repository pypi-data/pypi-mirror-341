# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateWifiProfileParcelForMobilityPostRequest,
    EditWifiProfileParcelForMobilityPutRequest,
    GetListMobilityGlobalWifiPayload,
    GetSingleMobilityGlobalWifiPayload,
)


class WifiBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/mobility/global/{profileId}/wifi
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, profile_id: str, payload: CreateWifiProfileParcelForMobilityPostRequest, **kw
    ) -> str:
        """
        Create an Wifi Profile Parcel for Mobility feature profile
        POST /dataservice/v1/feature-profile/mobility/global/{profileId}/wifi

        :param profile_id: Feature Profile ID
        :param payload: Wifi Profile Parcel
        :returns: str
        """
        params = {
            "profileId": profile_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/wifi",
            return_type=str,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        profile_id: str,
        wifi_id: str,
        payload: EditWifiProfileParcelForMobilityPutRequest,
        **kw,
    ):
        """
        Edit an Wifi Profile Parcel for Mobility feature profile
        PUT /dataservice/v1/feature-profile/mobility/global/{profileId}/wifi/{wifiId}

        :param profile_id: Feature Profile ID
        :param wifi_id: Profile Parcel ID
        :param payload: Wifi Profile Parcel
        :returns: None
        """
        params = {
            "profileId": profile_id,
            "wifiId": wifi_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/wifi/{wifiId}",
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, profile_id: str, wifi_id: str, **kw):
        """
        Delete an Wifi Profile Parcel for Mobility feature profile
        DELETE /dataservice/v1/feature-profile/mobility/global/{profileId}/wifi/{wifiId}

        :param profile_id: Feature Profile ID
        :param wifi_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "profileId": profile_id,
            "wifiId": wifi_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/wifi/{wifiId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, profile_id: str, wifi_id: str, **kw) -> GetSingleMobilityGlobalWifiPayload:
        """
        Get an Wifi Profile Parcel for Mobility feature profile
        GET /dataservice/v1/feature-profile/mobility/global/{profileId}/wifi/{wifiId}

        :param profile_id: Feature Profile ID
        :param wifi_id: Profile Parcel ID
        :returns: GetSingleMobilityGlobalWifiPayload
        """
        ...

    @overload
    def get(self, profile_id: str, **kw) -> GetListMobilityGlobalWifiPayload:
        """
        Get Wifi Profile Parcel List for Mobility feature profile
        GET /dataservice/v1/feature-profile/mobility/global/{profileId}/wifi

        :param profile_id: Feature Profile ID
        :returns: GetListMobilityGlobalWifiPayload
        """
        ...

    def get(
        self, profile_id: str, wifi_id: Optional[str] = None, **kw
    ) -> Union[GetListMobilityGlobalWifiPayload, GetSingleMobilityGlobalWifiPayload]:
        # /dataservice/v1/feature-profile/mobility/global/{profileId}/wifi/{wifiId}
        if self._request_adapter.param_checker([(profile_id, str), (wifi_id, str)], []):
            params = {
                "profileId": profile_id,
                "wifiId": wifi_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{profileId}/wifi/{wifiId}",
                return_type=GetSingleMobilityGlobalWifiPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/mobility/global/{profileId}/wifi
        if self._request_adapter.param_checker([(profile_id, str)], [wifi_id]):
            params = {
                "profileId": profile_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{profileId}/wifi",
                return_type=GetListMobilityGlobalWifiPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
