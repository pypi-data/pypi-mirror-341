# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import QoSRespWithPageInfo


class PageBuilder:
    """
    Builds and executes requests for operations under /statistics/qos/page
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        query: Optional[str] = None,
        scroll_id: Optional[str] = None,
        count: Optional[int] = None,
        **kw,
    ) -> QoSRespWithPageInfo:
        """
        Get stats raw data
        GET /dataservice/statistics/qos/page

        :param query: Query
        :param scroll_id: Scroll id
        :param count: Count
        :returns: QoSRespWithPageInfo
        """
        params = {
            "query": query,
            "scrollId": scroll_id,
            "count": count,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/qos/page",
            return_type=QoSRespWithPageInfo,
            params=params,
            **kw,
        )

    def post(
        self, payload: Any, scroll_id: Optional[str] = None, count: Optional[int] = None, **kw
    ) -> QoSRespWithPageInfo:
        """
        Get stats raw data
        POST /dataservice/statistics/qos/page

        :param scroll_id: Scroll id
        :param count: Count
        :param payload: Stats query string
        :returns: QoSRespWithPageInfo
        """
        params = {
            "scrollId": scroll_id,
            "count": count,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/qos/page",
            return_type=QoSRespWithPageInfo,
            params=params,
            payload=payload,
            **kw,
        )
