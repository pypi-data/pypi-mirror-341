# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateNfvirtualSystemFeatureProfilePostRequest,
    CreateNfvirtualSystemFeatureProfilePostResponse,
    EditNfvirtualSystemFeatureProfilePutRequest,
    EditNfvirtualSystemFeatureProfilePutResponse,
    GetAllNfvirtualSystemFeatureProfilesGetResponse,
    GetSingleNfvirtualSystemPayload,
)

if TYPE_CHECKING:
    from .aaa.aaa_builder import AaaBuilder
    from .banner.banner_builder import BannerBuilder
    from .logging.logging_builder import LoggingBuilder
    from .ntp.ntp_builder import NtpBuilder
    from .snmp.snmp_builder import SnmpBuilder
    from .system_settings.system_settings_builder import SystemSettingsBuilder


class SystemBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/nfvirtual/system
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, payload: CreateNfvirtualSystemFeatureProfilePostRequest, **kw
    ) -> CreateNfvirtualSystemFeatureProfilePostResponse:
        """
        Create a nfvirtual System Feature Profile
        POST /dataservice/v1/feature-profile/nfvirtual/system

        :param payload: Nfvirtual Feature profile
        :returns: CreateNfvirtualSystemFeatureProfilePostResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/nfvirtual/system",
            return_type=CreateNfvirtualSystemFeatureProfilePostResponse,
            payload=payload,
            **kw,
        )

    def put(
        self, system_id: str, payload: EditNfvirtualSystemFeatureProfilePutRequest, **kw
    ) -> EditNfvirtualSystemFeatureProfilePutResponse:
        """
        Edit a Nfvirtual System Feature Profile
        PUT /dataservice/v1/feature-profile/nfvirtual/system/{systemId}

        :param system_id: Feature Profile Id
        :param payload: Nfvirtual Feature profile
        :returns: EditNfvirtualSystemFeatureProfilePutResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}",
            return_type=EditNfvirtualSystemFeatureProfilePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, **kw):
        """
        Delete a Nfvirtual System Feature Profile
        DELETE /dataservice/v1/feature-profile/nfvirtual/system/{systemId}

        :param system_id: Feature Profile Id
        :returns: None
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, *, system_id: str, **kw) -> GetSingleNfvirtualSystemPayload:
        """
        Get a Nfvirtual System Feature Profile with systemId
        GET /dataservice/v1/feature-profile/nfvirtual/system/{systemId}

        :param system_id: Feature Profile Id
        :returns: GetSingleNfvirtualSystemPayload
        """
        ...

    @overload
    def get(
        self, *, offset: Optional[int] = None, limit: Optional[int] = 0, **kw
    ) -> List[GetAllNfvirtualSystemFeatureProfilesGetResponse]:
        """
        Get all Nfvirtual System Feature Profiles
        GET /dataservice/v1/feature-profile/nfvirtual/system

        :param offset: Pagination offset
        :param limit: Pagination limit
        :returns: List[GetAllNfvirtualSystemFeatureProfilesGetResponse]
        """
        ...

    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        system_id: Optional[str] = None,
        **kw,
    ) -> Union[
        List[GetAllNfvirtualSystemFeatureProfilesGetResponse], GetSingleNfvirtualSystemPayload
    ]:
        # /dataservice/v1/feature-profile/nfvirtual/system/{systemId}
        if self._request_adapter.param_checker([(system_id, str)], [offset, limit]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}",
                return_type=GetSingleNfvirtualSystemPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/nfvirtual/system
        if self._request_adapter.param_checker([], [system_id]):
            params = {
                "offset": offset,
                "limit": limit,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/nfvirtual/system",
                return_type=List[GetAllNfvirtualSystemFeatureProfilesGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def aaa(self) -> AaaBuilder:
        """
        The aaa property
        """
        from .aaa.aaa_builder import AaaBuilder

        return AaaBuilder(self._request_adapter)

    @property
    def banner(self) -> BannerBuilder:
        """
        The banner property
        """
        from .banner.banner_builder import BannerBuilder

        return BannerBuilder(self._request_adapter)

    @property
    def logging(self) -> LoggingBuilder:
        """
        The logging property
        """
        from .logging.logging_builder import LoggingBuilder

        return LoggingBuilder(self._request_adapter)

    @property
    def ntp(self) -> NtpBuilder:
        """
        The ntp property
        """
        from .ntp.ntp_builder import NtpBuilder

        return NtpBuilder(self._request_adapter)

    @property
    def snmp(self) -> SnmpBuilder:
        """
        The snmp property
        """
        from .snmp.snmp_builder import SnmpBuilder

        return SnmpBuilder(self._request_adapter)

    @property
    def system_settings(self) -> SystemSettingsBuilder:
        """
        The system-settings property
        """
        from .system_settings.system_settings_builder import SystemSettingsBuilder

        return SystemSettingsBuilder(self._request_adapter)
