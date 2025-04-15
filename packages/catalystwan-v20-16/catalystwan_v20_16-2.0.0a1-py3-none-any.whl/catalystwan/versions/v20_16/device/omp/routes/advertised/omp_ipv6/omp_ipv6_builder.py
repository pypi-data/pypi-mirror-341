# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class OmpIpv6Builder:
    """
    Builds and executes requests for operations under /device/omp/routes/advertised/ompIpv6
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> List[Any]:
        """
        Get OMP advertised routes list (Real Time)
        GET /dataservice/device/omp/routes/advertised/ompIpv6

        :param device_id: deviceId - Device IP
        :returns: List[Any]
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/omp/routes/advertised/ompIpv6",
            return_type=List[Any],
            params=params,
            **kw,
        )
