# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class GetClientIdBuilder:
    """
    Builds and executes requests for operations under /opentaccase/getClientID
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Gets vManage Client ID
        GET /dataservice/opentaccase/getClientID

        :returns: List[Any]
        """
        logging.warning("Operation: %s is deprecated", "getClientID")
        return self._request_adapter.request(
            "GET", "/dataservice/opentaccase/getClientID", return_type=List[Any], **kw
        )
