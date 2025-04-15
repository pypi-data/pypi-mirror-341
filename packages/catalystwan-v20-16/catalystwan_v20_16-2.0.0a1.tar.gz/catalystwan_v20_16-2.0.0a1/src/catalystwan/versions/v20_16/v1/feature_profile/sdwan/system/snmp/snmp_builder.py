# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSnmpProfileParcelForSystemPostRequest,
    CreateSnmpProfileParcelForSystemPostResponse,
    EditSnmpProfileParcelForSystemPutRequest,
    EditSnmpProfileParcelForSystemPutResponse,
    GetListSdwanSystemSnmpPayload,
    GetSingleSdwanSystemSnmpPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class SnmpBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/system/snmp
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateSnmpProfileParcelForSystemPostRequest, **kw
    ) -> CreateSnmpProfileParcelForSystemPostResponse:
        """
        Create a Snmp Profile Parcel for System feature profile
        POST /dataservice/v1/feature-profile/sdwan/system/{systemId}/snmp

        :param system_id: Feature Profile ID
        :param payload: Snmp Profile Parcel
        :returns: CreateSnmpProfileParcelForSystemPostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/snmp",
            return_type=CreateSnmpProfileParcelForSystemPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self, system_id: str, snmp_id: str, payload: EditSnmpProfileParcelForSystemPutRequest, **kw
    ) -> EditSnmpProfileParcelForSystemPutResponse:
        """
        Update a Snmp Profile Parcel for System feature profile
        PUT /dataservice/v1/feature-profile/sdwan/system/{systemId}/snmp/{snmpId}

        :param system_id: Feature Profile ID
        :param snmp_id: Profile Parcel ID
        :param payload: Snmp Profile Parcel
        :returns: EditSnmpProfileParcelForSystemPutResponse
        """
        params = {
            "systemId": system_id,
            "snmpId": snmp_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/snmp/{snmpId}",
            return_type=EditSnmpProfileParcelForSystemPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, snmp_id: str, **kw):
        """
        Delete a Snmp Profile Parcel for System feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/system/{systemId}/snmp/{snmpId}

        :param system_id: Feature Profile ID
        :param snmp_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "systemId": system_id,
            "snmpId": snmp_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/snmp/{snmpId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, system_id: str, snmp_id: str, **kw) -> GetSingleSdwanSystemSnmpPayload:
        """
        Get Snmp Profile Parcel by parcelId for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/snmp/{snmpId}

        :param system_id: Feature Profile ID
        :param snmp_id: Profile Parcel ID
        :returns: GetSingleSdwanSystemSnmpPayload
        """
        ...

    @overload
    def get(self, system_id: str, **kw) -> GetListSdwanSystemSnmpPayload:
        """
        Get Snmp Profile Parcels for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/snmp

        :param system_id: Feature Profile ID
        :returns: GetListSdwanSystemSnmpPayload
        """
        ...

    def get(
        self, system_id: str, snmp_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanSystemSnmpPayload, GetSingleSdwanSystemSnmpPayload]:
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/snmp/{snmpId}
        if self._request_adapter.param_checker([(system_id, str), (snmp_id, str)], []):
            params = {
                "systemId": system_id,
                "snmpId": snmp_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/snmp/{snmpId}",
                return_type=GetSingleSdwanSystemSnmpPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/snmp
        if self._request_adapter.param_checker([(system_id, str)], [snmp_id]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/snmp",
                return_type=GetListSdwanSystemSnmpPayload,
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
