# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface


class ActionsBuilder:
    """
    Builds and executes requests for operations under /fedramp/wazuh/actions
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, action: Optional[str] = None, **kw) -> List[Any]:
        """
        Wazuh agent action
        GET /dataservice/fedramp/wazuh/actions

        :param action: Wazhuh Action
        :returns: List[Any]
        """
        params = {
            "action": action,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/fedramp/wazuh/actions", return_type=List[Any], params=params, **kw
        )
