# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class DoccountBuilder:
    """
    Builds and executes requests for operations under /data/device/statistics/{state_data_type}/doccount
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        state_data_type: str,
        start_date: str,
        end_date: str,
        time_zone: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get response count of a query
        GET /dataservice/data/device/statistics/{state_data_type}/doccount

        :param state_data_type: State data type(example:object)
        :param start_date: Start date (example:2023-10-31T14:30:00)
        :param end_date: End date (example:2023-10-31T14:30:00)
        :param time_zone: Time zone (example:UTC)
        :returns: Any
        """
        params = {
            "state_data_type": state_data_type,
            "startDate": start_date,
            "endDate": end_date,
            "timeZone": time_zone,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/data/device/statistics/{state_data_type}/doccount",
            params=params,
            **kw,
        )
