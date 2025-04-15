# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class DoesValidImageExistBuilder:
    """
    Builds and executes requests for operations under /container-manager/doesValidImageExist
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, container_name: str, **kw) -> Any:
        """
        Get container image checksum
        GET /dataservice/container-manager/doesValidImageExist/{containerName}

        :param container_name: Container name
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "doesValidImageExist")
        params = {
            "containerName": container_name,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/container-manager/doesValidImageExist/{containerName}",
            params=params,
            **kw,
        )
