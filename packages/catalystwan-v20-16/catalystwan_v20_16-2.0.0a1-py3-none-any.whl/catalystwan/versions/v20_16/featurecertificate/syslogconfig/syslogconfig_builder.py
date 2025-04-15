# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class SyslogconfigBuilder:
    """
    Builds and executes requests for operations under /featurecertificate/syslogconfig
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get Feature CA state


        Note: In a multitenant vManage system, this API is only available in the Provider and Provider-As-Tenant view.
        GET /dataservice/featurecertificate/syslogconfig

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/featurecertificate/syslogconfig", **kw
        )
