# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class AddcloudxBuilder:
    """
    Builds and executes requests for operations under /template/cloudx/addcloudx
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, type_: str, payload: Any, **kw):
        """
        Add cloudx gateway
        POST /dataservice/template/cloudx/addcloudx/{type}

        :param type_: Cloudx type
        :param payload: Cloudx
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "addCloudxType")
        params = {
            "type": type_,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/template/cloudx/addcloudx/{type}",
            params=params,
            payload=payload,
            **kw,
        )
