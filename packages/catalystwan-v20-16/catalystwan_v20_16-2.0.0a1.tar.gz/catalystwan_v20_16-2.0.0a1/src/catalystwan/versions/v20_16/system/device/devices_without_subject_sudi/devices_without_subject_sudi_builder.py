# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class DevicesWithoutSubjectSudiBuilder:
    """
    Builds and executes requests for operations under /system/device/devicesWithoutSubjectSudi
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        retrieve devices without subject sudi
        GET /dataservice/system/device/devicesWithoutSubjectSudi

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/system/device/devicesWithoutSubjectSudi",
            return_type=List[Any],
            **kw,
        )
