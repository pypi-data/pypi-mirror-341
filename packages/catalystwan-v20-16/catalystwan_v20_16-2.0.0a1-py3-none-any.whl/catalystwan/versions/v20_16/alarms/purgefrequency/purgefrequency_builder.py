# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import PurgeFrequency


class PurgefrequencyBuilder:
    """
    Builds and executes requests for operations under /alarms/purgefrequency
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, interval: Optional[str] = None, active_time: Optional[str] = None, **kw
    ) -> PurgeFrequency:
        """
        Set alarm purge timer
        GET /dataservice/alarms/purgefrequency

        :param interval: Purge interval
        :param active_time: Active time
        :returns: PurgeFrequency
        """
        params = {
            "interval": interval,
            "activeTime": active_time,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/alarms/purgefrequency",
            return_type=PurgeFrequency,
            params=params,
            **kw,
        )
