# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class ApplicationBuilder:
    """
    Builds and executes requests for operations under /app-registry/application
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, app_uuid: str, **kw) -> List[Any]:
        """
        Get  app detail for particular App uuid
        GET /dataservice/app-registry/application/{app-uuid}

        :param app_uuid: App uuid
        :returns: List[Any]
        """
        params = {
            "app-uuid": app_uuid,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/app-registry/application/{app-uuid}",
            return_type=List[Any],
            params=params,
            **kw,
        )
