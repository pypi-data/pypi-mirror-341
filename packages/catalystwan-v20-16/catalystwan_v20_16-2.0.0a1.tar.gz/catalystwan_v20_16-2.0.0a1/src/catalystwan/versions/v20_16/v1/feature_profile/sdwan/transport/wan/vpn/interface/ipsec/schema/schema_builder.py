# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SchemaTypeParam


class SchemaBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/wan/vpn/interface/ipsec/schema
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, schema_type: SchemaTypeParam, **kw) -> str:
        """
        Get a SDWAN Transport WanVpn InterfaceIpsec Schema by Schema Type
        GET /dataservice/v1/feature-profile/sdwan/transport/wan/vpn/interface/ipsec/schema

        :param schema_type: Schema type
        :returns: str
        """
        params = {
            "schemaType": schema_type,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/sdwan/transport/wan/vpn/interface/ipsec/schema",
            return_type=str,
            params=params,
            **kw,
        )
