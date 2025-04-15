# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateNfvirtualCliParcelPostRequest,
    CreateNfvirtualCliParcelPostResponse,
    EditNfvirtualCliParcelPutRequest,
    EditNfvirtualCliParcelPutResponse,
    GetSingleNfvirtualCliConfigPayload,
)


class ConfigBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/nfvirtual/cli/{cliId}/config
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, cli_id: str, payload: CreateNfvirtualCliParcelPostRequest, **kw
    ) -> CreateNfvirtualCliParcelPostResponse:
        """
        Create CLI Profile Parcel for CLI feature profile
        POST /dataservice/v1/feature-profile/nfvirtual/cli/{cliId}/config

        :param cli_id: CLI Feature Profile ID
        :param payload: CLI Profile Parcel
        :returns: CreateNfvirtualCliParcelPostResponse
        """
        params = {
            "cliId": cli_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/nfvirtual/cli/{cliId}/config",
            return_type=CreateNfvirtualCliParcelPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def get(self, cli_id: str, config_id: str, **kw) -> GetSingleNfvirtualCliConfigPayload:
        """
        Get CLI Profile Parcels for CLI feature profile
        GET /dataservice/v1/feature-profile/nfvirtual/cli/{cliId}/config/{configId}

        :param cli_id: CLI Feature Profile ID
        :param config_id: CLI Parcel ID
        :returns: GetSingleNfvirtualCliConfigPayload
        """
        params = {
            "cliId": cli_id,
            "configId": config_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/nfvirtual/cli/{cliId}/config/{configId}",
            return_type=GetSingleNfvirtualCliConfigPayload,
            params=params,
            **kw,
        )

    def put(
        self, cli_id: str, config_id: str, payload: EditNfvirtualCliParcelPutRequest, **kw
    ) -> EditNfvirtualCliParcelPutResponse:
        """
        Edit CLI Profile Parcel for CLI feature profile
        PUT /dataservice/v1/feature-profile/nfvirtual/cli/{cliId}/config/{configId}

        :param cli_id: CLI Feature Profile ID
        :param config_id: CLI Parcel ID
        :param payload: CLI Profile Parcel
        :returns: EditNfvirtualCliParcelPutResponse
        """
        params = {
            "cliId": cli_id,
            "configId": config_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/nfvirtual/cli/{cliId}/config/{configId}",
            return_type=EditNfvirtualCliParcelPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, cli_id: str, config_id: str, **kw):
        """
        Delete CLI Profile Parcel for CLI feature profile
        DELETE /dataservice/v1/feature-profile/nfvirtual/cli/{cliId}/config/{configId}

        :param cli_id: CLI Feature Profile ID
        :param config_id: CLI Parcel ID
        :returns: None
        """
        params = {
            "cliId": cli_id,
            "configId": config_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/nfvirtual/cli/{cliId}/config/{configId}",
            params=params,
            **kw,
        )
