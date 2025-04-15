# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateNfvirtualSystemSettingsParcelPostRequest,
    CreateNfvirtualSystemSettingsParcelPostResponse,
    EditNfvirtualSystemSettingsParcelPutRequest,
    EditNfvirtualSystemSettingsParcelPutResponse,
    GetSingleNfvirtualSystemSystemSettingsPayload,
)


class SystemSettingsBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/nfvirtual/system/{systemId}/system-settings
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateNfvirtualSystemSettingsParcelPostRequest, **kw
    ) -> CreateNfvirtualSystemSettingsParcelPostResponse:
        """
        Create System settings  Profile Parcel for System feature profile
        POST /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/system-settings

        :param system_id: Feature Profile ID
        :param payload: System Settings  config Profile Parcel
        :returns: CreateNfvirtualSystemSettingsParcelPostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/system-settings",
            return_type=CreateNfvirtualSystemSettingsParcelPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def get(
        self, system_id: str, system_settings_id: str, **kw
    ) -> GetSingleNfvirtualSystemSystemSettingsPayload:
        """
        Get System Settings Profile Parcels for System feature profile
        GET /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/system-settings/{systemSettingsId}

        :param system_id: Feature Profile ID
        :param system_settings_id: Profile Parcel ID
        :returns: GetSingleNfvirtualSystemSystemSettingsPayload
        """
        params = {
            "systemId": system_id,
            "systemSettingsId": system_settings_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/system-settings/{systemSettingsId}",
            return_type=GetSingleNfvirtualSystemSystemSettingsPayload,
            params=params,
            **kw,
        )

    def put(
        self,
        system_id: str,
        system_settings_id: str,
        payload: EditNfvirtualSystemSettingsParcelPutRequest,
        **kw,
    ) -> EditNfvirtualSystemSettingsParcelPutResponse:
        """
        Edit a System Settings Profile Parcel for System feature profile
        PUT /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/system-settings/{systemSettingsId}

        :param system_id: Feature Profile ID
        :param system_settings_id: Profile Parcel ID
        :param payload: System Settings Profile Parcel
        :returns: EditNfvirtualSystemSettingsParcelPutResponse
        """
        params = {
            "systemId": system_id,
            "systemSettingsId": system_settings_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/system-settings/{systemSettingsId}",
            return_type=EditNfvirtualSystemSettingsParcelPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, system_settings_id: str, **kw):
        """
        Delete System settings Profile Parcel for System feature profile
        DELETE /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/system-settings/{systemSettingsId}

        :param system_id: Feature Profile ID
        :param system_settings_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "systemId": system_id,
            "systemSettingsId": system_settings_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/system-settings/{systemSettingsId}",
            params=params,
            **kw,
        )
