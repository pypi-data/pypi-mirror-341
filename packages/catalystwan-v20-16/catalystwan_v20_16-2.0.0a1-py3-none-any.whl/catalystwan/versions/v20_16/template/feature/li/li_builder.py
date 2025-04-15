# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class LiBuilder:
    """
    Builds and executes requests for operations under /template/feature/li
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get LI feature template
        GET /dataservice/template/feature/li

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/template/feature/li", return_type=List[Any], **kw
        )

    def post(self, payload: Any, **kw) -> Any:
        """
        Create LI feature template


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        POST /dataservice/template/feature/li

        :param payload: LI template
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/template/feature/li", payload=payload, **kw
        )

    def put(self, template_id: str, payload: Any, **kw) -> Any:
        """
        Update LI feature template


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        PUT /dataservice/template/feature/li/{templateId}

        :param template_id: Template Id
        :param payload: LI template
        :returns: Any
        """
        params = {
            "templateId": template_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/template/feature/li/{templateId}",
            params=params,
            payload=payload,
            **kw,
        )
