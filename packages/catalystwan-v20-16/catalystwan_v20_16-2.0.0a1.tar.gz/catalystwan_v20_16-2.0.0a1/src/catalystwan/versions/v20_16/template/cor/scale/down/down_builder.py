# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class DownBuilder:
    """
    Builds and executes requests for operations under /template/cor/scale/down
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw):
        """
        Scale down cloud on ramp
        POST /dataservice/template/cor/scale/down

        :param payload: Update VPC
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "scaleDown")
        return self._request_adapter.request(
            "POST", "/dataservice/template/cor/scale/down", payload=payload, **kw
        )
