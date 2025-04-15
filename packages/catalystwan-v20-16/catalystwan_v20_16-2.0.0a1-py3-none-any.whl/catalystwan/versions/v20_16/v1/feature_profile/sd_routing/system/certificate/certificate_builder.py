# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingCertificateFeaturePostRequest,
    CreateSdroutingCertificateFeaturePostResponse,
    EditSdroutingCertificateFeaturePutRequest,
    EditSdroutingCertificateFeaturePutResponse,
    GetListSdRoutingSystemCertificatePayload,
    GetSingleSdRoutingSystemCertificatePayload,
)


class CertificateBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/system/{systemId}/certificate
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateSdroutingCertificateFeaturePostRequest, **kw
    ) -> CreateSdroutingCertificateFeaturePostResponse:
        """
        Create a SD-Routing certificate feature from a specific system feature profile
        POST /dataservice/v1/feature-profile/sd-routing/system/{systemId}/certificate

        :param system_id: System Profile ID
        :param payload: SD-Routing certificate feature from a specific system feature profile
        :returns: CreateSdroutingCertificateFeaturePostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/certificate",
            return_type=CreateSdroutingCertificateFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        system_id: str,
        certificate_id: str,
        payload: EditSdroutingCertificateFeaturePutRequest,
        **kw,
    ) -> EditSdroutingCertificateFeaturePutResponse:
        """
        Edit the SD-Routing certificate feature from a specific system feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/system/{systemId}/certificate/{certificateId}

        :param system_id: System Profile ID
        :param certificate_id: Certificate Feature ID
        :param payload: SD-Routing certificate feature from a specific system feature profile
        :returns: EditSdroutingCertificateFeaturePutResponse
        """
        params = {
            "systemId": system_id,
            "certificateId": certificate_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/certificate/{certificateId}",
            return_type=EditSdroutingCertificateFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, certificate_id: str, **kw):
        """
        Delete the SD-Routing certificate feature from a specific system feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/system/{systemId}/certificate/{certificateId}

        :param system_id: System Profile ID
        :param certificate_id: Certificate Feature ID
        :returns: None
        """
        params = {
            "systemId": system_id,
            "certificateId": certificate_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/certificate/{certificateId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, system_id: str, certificate_id: str, **kw
    ) -> GetSingleSdRoutingSystemCertificatePayload:
        """
        Get the SD-Routing certificate feature from a specific system feature profile
        GET /dataservice/v1/feature-profile/sd-routing/system/{systemId}/certificate/{certificateId}

        :param system_id: System Profile ID
        :param certificate_id: Certificate Feature ID
        :returns: GetSingleSdRoutingSystemCertificatePayload
        """
        ...

    @overload
    def get(self, system_id: str, **kw) -> GetListSdRoutingSystemCertificatePayload:
        """
        Get all SD-Routing certificate features from a specific system feature profile
        GET /dataservice/v1/feature-profile/sd-routing/system/{systemId}/certificate

        :param system_id: System Profile ID
        :returns: GetListSdRoutingSystemCertificatePayload
        """
        ...

    def get(
        self, system_id: str, certificate_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingSystemCertificatePayload, GetSingleSdRoutingSystemCertificatePayload
    ]:
        # /dataservice/v1/feature-profile/sd-routing/system/{systemId}/certificate/{certificateId}
        if self._request_adapter.param_checker([(system_id, str), (certificate_id, str)], []):
            params = {
                "systemId": system_id,
                "certificateId": certificate_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/certificate/{certificateId}",
                return_type=GetSingleSdRoutingSystemCertificatePayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/system/{systemId}/certificate
        if self._request_adapter.param_checker([(system_id, str)], [certificate_id]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/certificate",
                return_type=GetListSdRoutingSystemCertificatePayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
