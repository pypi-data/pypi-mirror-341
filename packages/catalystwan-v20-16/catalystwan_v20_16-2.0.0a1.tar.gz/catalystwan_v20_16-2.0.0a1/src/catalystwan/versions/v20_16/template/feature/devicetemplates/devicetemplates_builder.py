# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class DevicetemplatesBuilder:
    """
    Builds and executes requests for operations under /template/feature/devicetemplates
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, template_id: str, **kw) -> Any:
        """
        Get all device templates for this feature template


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/template/feature/devicetemplates/{templateId}

        :param template_id: Feature template Id
        :returns: Any
        """
        params = {
            "templateId": template_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/template/feature/devicetemplates/{templateId}", params=params, **kw
        )
