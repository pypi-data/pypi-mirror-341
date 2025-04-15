# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class RulesBuilder:
    """
    Builds and executes requests for operations under /v1/config-group/{configGroupId}/rules
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, config_group_id: str, **kw) -> str:
        """
        Get Rule by associated object Id, example : get rules by config group Id
        GET /dataservice/v1/config-group/{configGroupId}/rules

        :param config_group_id: Config group id
        :returns: str
        """
        params = {
            "configGroupId": config_group_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/config-group/{configGroupId}/rules",
            return_type=str,
            params=params,
            **kw,
        )
