# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class AppsBuilder:
    """
    Builds and executes requests for operations under /template/cloudx/manage/apps
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get apps and vpns
        GET /dataservice/template/cloudx/manage/apps

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/template/cloudx/manage/apps", return_type=List[Any], **kw
        )

    def put(self, payload: Any, **kw) -> Any:
        """
        Edit apps and vpns
        PUT /dataservice/template/cloudx/manage/apps

        :param payload: Cloudx apps and vpns
        :returns: Any
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/template/cloudx/manage/apps", payload=payload, **kw
        )

    def post(self, payload: Any, **kw) -> List[Any]:
        """
        Add apps and vpns
        POST /dataservice/template/cloudx/manage/apps

        :param payload: Cloudx apps and vpns
        :returns: List[Any]
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/template/cloudx/manage/apps",
            return_type=List[Any],
            payload=payload,
            **kw,
        )
