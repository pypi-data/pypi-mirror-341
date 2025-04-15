# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class SchemaBuilder:
    """
    Builds and executes requests for operations under /v1/config-group/{configGroupId}/device/variables/schema
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, config_group_id: str, all: Optional[bool] = False, **kw) -> Any:
        """
        get device variables schema
        GET /dataservice/v1/config-group/{configGroupId}/device/variables/schema

        :param config_group_id: Config Group Id
        :param all: All variables(including sub-feature)
        :returns: Any
        """
        params = {
            "configGroupId": config_group_id,
            "all": all,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/config-group/{configGroupId}/device/variables/schema",
            params=params,
            **kw,
        )
