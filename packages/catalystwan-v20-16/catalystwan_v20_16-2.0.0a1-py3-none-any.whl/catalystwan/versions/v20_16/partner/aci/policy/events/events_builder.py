# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface


class EventsBuilder:
    """
    Builds and executes requests for operations under /partner/aci/policy/events
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, partner_id: str, starttime: Optional[int] = None, endtime: Optional[int] = None, **kw
    ) -> List[Any]:
        """
        Get ACI events
        GET /dataservice/partner/aci/policy/events/{partnerId}

        :param partner_id: Partner Id
        :param starttime: Start time
        :param endtime: End time
        :returns: List[Any]
        """
        params = {
            "partnerId": partner_id,
            "starttime": starttime,
            "endtime": endtime,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/partner/aci/policy/events/{partnerId}",
            return_type=List[Any],
            params=params,
            **kw,
        )
