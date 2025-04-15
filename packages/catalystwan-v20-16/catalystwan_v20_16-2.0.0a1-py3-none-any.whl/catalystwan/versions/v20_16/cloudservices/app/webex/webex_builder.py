# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface


class WebexBuilder:
    """
    Builds and executes requests for operations under /cloudservices/app/webex
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, payload: Any, **kw) -> List[Any]:
        """
        Day N- Update Webex App
        PUT /dataservice/cloudservices/app/webex

        :param payload: Cloudx apps and vpns
        :returns: List[Any]
        """
        return self._request_adapter.request(
            "PUT",
            "/dataservice/cloudservices/app/webex",
            return_type=List[Any],
            payload=payload,
            **kw,
        )

    def post(self, payload: Any, **kw) -> List[Any]:
        """
        Add Webex App
        POST /dataservice/cloudservices/app/webex

        :param payload: Cloudx apps and vpns
        :returns: List[Any]
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/cloudservices/app/webex",
            return_type=List[Any],
            payload=payload,
            **kw,
        )

    def delete(self, payload: Optional[Any] = None, **kw) -> List[Any]:
        """
        deleteWebexPrefixLists
        DELETE /dataservice/cloudservices/app/webex

        :param payload: TMP-Cloudx apps and vpns
        :returns: List[Any]
        """
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/cloudservices/app/webex",
            return_type=List[Any],
            payload=payload,
            **kw,
        )
