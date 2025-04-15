# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface


class ActiveBuilder:
    """
    Builds and executes requests for operations under /data/device/statistics/alarm/active
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        scroll_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        count: Optional[int] = None,
        time_zone: Optional[str] = None,
        **kw,
    ) -> List[Any]:
        """
        Get active alarms
        GET /dataservice/data/device/statistics/alarm/active

        :param scroll_id: SrollId
        :param start_date: Start date (example:2023-10-31T14:30:00)
        :param end_date: End date (example:2023-10-31T14:30:00)
        :param count: count
        :param time_zone: Time zone
        :returns: List[Any]
        """
        params = {
            "scrollId": scroll_id,
            "startDate": start_date,
            "endDate": end_date,
            "count": count,
            "timeZone": time_zone,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/data/device/statistics/alarm/active",
            return_type=List[Any],
            params=params,
            **kw,
        )
