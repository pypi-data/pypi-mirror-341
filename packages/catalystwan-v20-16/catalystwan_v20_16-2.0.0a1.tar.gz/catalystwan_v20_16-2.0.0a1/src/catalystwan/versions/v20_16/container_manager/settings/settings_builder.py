# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class SettingsBuilder:
    """
    Builds and executes requests for operations under /container-manager/settings
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, container_name: str, host_ip: Optional[str] = None, **kw) -> Any:
        """
        Get container settings
        GET /dataservice/container-manager/settings/{containerName}

        :param container_name: Container name
        :param host_ip: Container host IP
        :returns: Any
        """
        params = {
            "containerName": container_name,
            "hostIp": host_ip,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/container-manager/settings/{containerName}", params=params, **kw
        )
