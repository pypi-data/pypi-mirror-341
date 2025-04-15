# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSecurityForSystemPostRequest,
    CreateSecurityForSystemPostResponse,
    EditSecurityForSystemPutRequest,
    EditSecurityForSystemPutResponse,
    GetListSdwanSystemSecurityPayload,
    GetSingleSdwanSystemSecurityPayload,
)


class SecurityBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/system/{systemId}/security
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateSecurityForSystemPostRequest, **kw
    ) -> CreateSecurityForSystemPostResponse:
        """
        Create Security for System feature profile
        POST /dataservice/v1/feature-profile/sdwan/system/{systemId}/security

        :param system_id: Feature Profile ID
        :param payload: Security Feature
        :returns: CreateSecurityForSystemPostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/security",
            return_type=CreateSecurityForSystemPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self, system_id: str, security_id: str, payload: EditSecurityForSystemPutRequest, **kw
    ) -> EditSecurityForSystemPutResponse:
        """
        Update Security for System feature profile
        PUT /dataservice/v1/feature-profile/sdwan/system/{systemId}/security/{securityId}

        :param system_id: Feature Profile ID
        :param security_id: Security ID
        :param payload: Security Feature
        :returns: EditSecurityForSystemPutResponse
        """
        params = {
            "systemId": system_id,
            "securityId": security_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/security/{securityId}",
            return_type=EditSecurityForSystemPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, security_id: str, **kw):
        """
        Delete Security for System feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/system/{systemId}/security/{securityId}

        :param system_id: Feature Profile ID
        :param security_id: Security ID
        :returns: None
        """
        params = {
            "systemId": system_id,
            "securityId": security_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/security/{securityId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, system_id: str, security_id: str, **kw) -> GetSingleSdwanSystemSecurityPayload:
        """
        Get Security by securityId for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/security/{securityId}

        :param system_id: Feature Profile ID
        :param security_id: Security ID
        :returns: GetSingleSdwanSystemSecurityPayload
        """
        ...

    @overload
    def get(self, system_id: str, **kw) -> GetListSdwanSystemSecurityPayload:
        """
        Get Security for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/security

        :param system_id: Feature Profile ID
        :returns: GetListSdwanSystemSecurityPayload
        """
        ...

    def get(
        self, system_id: str, security_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanSystemSecurityPayload, GetSingleSdwanSystemSecurityPayload]:
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/security/{securityId}
        if self._request_adapter.param_checker([(system_id, str), (security_id, str)], []):
            params = {
                "systemId": system_id,
                "securityId": security_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/security/{securityId}",
                return_type=GetSingleSdwanSystemSecurityPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/security
        if self._request_adapter.param_checker([(system_id, str)], [security_id]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/security",
                return_type=GetListSdwanSystemSecurityPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
