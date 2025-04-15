# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import Tokens


class TokenBuilder:
    """
    Builds and executes requests for operations under /token
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, client_id: str, region_base_uri: str, **kw) -> Tokens:
        """
        Get Access Token and Refresh Token for authorized user
        POST /dataservice/token/{regionBaseUri}/{clientId}

        :param client_id: Client id
        :param region_base_uri: Region base uri
        :returns: Tokens
        """
        params = {
            "clientId": client_id,
            "regionBaseUri": region_base_uri,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/token/{regionBaseUri}/{clientId}",
            return_type=Tokens,
            params=params,
            **kw,
        )
