# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdwanConfigProfileParcelForCliPostRequest,
    CreateSdwanConfigProfileParcelForCliPostResponse,
    EditConfigProfileParcelForCliPutRequest,
    EditConfigProfileParcelForCliPutResponse,
    GetListSdwanCliConfigPayload,
    GetSingleSdwanCliConfigPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class ConfigBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/cli/config
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, cli_id: str, payload: CreateSdwanConfigProfileParcelForCliPostRequest, **kw
    ) -> CreateSdwanConfigProfileParcelForCliPostResponse:
        """
        Create a config Profile Parcel for cli feature profile
        POST /dataservice/v1/feature-profile/sdwan/cli/{cliId}/config

        :param cli_id: Feature Profile ID
        :param payload: cli config Profile Parcel
        :returns: CreateSdwanConfigProfileParcelForCliPostResponse
        """
        params = {
            "cliId": cli_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/cli/{cliId}/config",
            return_type=CreateSdwanConfigProfileParcelForCliPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self, cli_id: str, config_id: str, payload: EditConfigProfileParcelForCliPutRequest, **kw
    ) -> EditConfigProfileParcelForCliPutResponse:
        """
        Update a config Profile Parcel for cli feature profile
        PUT /dataservice/v1/feature-profile/sdwan/cli/{cliId}/config/{configId}

        :param cli_id: Feature Profile ID
        :param config_id: Profile Parcel ID
        :param payload: cli config Profile Parcel
        :returns: EditConfigProfileParcelForCliPutResponse
        """
        params = {
            "cliId": cli_id,
            "configId": config_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/cli/{cliId}/config/{configId}",
            return_type=EditConfigProfileParcelForCliPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, cli_id: str, config_id: str, **kw):
        """
        Delete a config Profile Parcel for cli feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/cli/{cliId}/config/{configId}

        :param cli_id: Feature Profile ID
        :param config_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "cliId": cli_id,
            "configId": config_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/cli/{cliId}/config/{configId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, cli_id: str, config_id: str, **kw) -> GetSingleSdwanCliConfigPayload:
        """
        Get config Profile Parcel by configId for cli feature profile
        GET /dataservice/v1/feature-profile/sdwan/cli/{cliId}/config/{configId}

        :param cli_id: Feature Profile ID
        :param config_id: Profile Parcel ID
        :returns: GetSingleSdwanCliConfigPayload
        """
        ...

    @overload
    def get(self, cli_id: str, **kw) -> GetListSdwanCliConfigPayload:
        """
        Get config Profile Parcels for cli feature profile
        GET /dataservice/v1/feature-profile/sdwan/cli/{cliId}/config

        :param cli_id: Feature Profile ID
        :returns: GetListSdwanCliConfigPayload
        """
        ...

    def get(
        self, cli_id: str, config_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanCliConfigPayload, GetSingleSdwanCliConfigPayload]:
        # /dataservice/v1/feature-profile/sdwan/cli/{cliId}/config/{configId}
        if self._request_adapter.param_checker([(cli_id, str), (config_id, str)], []):
            params = {
                "cliId": cli_id,
                "configId": config_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/cli/{cliId}/config/{configId}",
                return_type=GetSingleSdwanCliConfigPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/cli/{cliId}/config
        if self._request_adapter.param_checker([(cli_id, str)], [config_id]):
            params = {
                "cliId": cli_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/cli/{cliId}/config",
                return_type=GetListSdwanCliConfigPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def schema(self) -> SchemaBuilder:
        """
        The schema property
        """
        from .schema.schema_builder import SchemaBuilder

        return SchemaBuilder(self._request_adapter)
