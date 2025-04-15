# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging

from catalystwan.abc import RequestAdapterInterface


class CountBuilder:
    """
    Builds and executes requests for operations under /colocation/monitor/vnf/alarms/count
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, user_group: str, **kw):
        """
        Get alarm count of VNF
        GET /dataservice/colocation/monitor/vnf/alarms/count

        :param user_group: User group
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "getVNFAlarmCount")
        params = {
            "user_group": user_group,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/colocation/monitor/vnf/alarms/count", params=params, **kw
        )
