# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class WaniBuilder:
    """
    Builds and executes requests for operations under /settings/configuration/wani
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Retrieve wani configuration value
        GET /dataservice/settings/configuration/wani

        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getWaniConfiguration")
        return self._request_adapter.request(
            "GET", "/dataservice/settings/configuration/wani", **kw
        )

    def put(self, payload: str, **kw) -> Any:
        """
        Update wani configuration setting
        PUT /dataservice/settings/configuration/wani

        :param payload: Payload
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "editWaniConfiguration")
        return self._request_adapter.request(
            "PUT", "/dataservice/settings/configuration/wani", payload=payload, **kw
        )

    def post(self, payload: str, **kw) -> str:
        """
        Add new wani configuration
        POST /dataservice/settings/configuration/wani

        :param payload: Payload
        :returns: str
        """
        logging.warning("Operation: %s is deprecated", "newWaniConfiguration")
        return self._request_adapter.request(
            "POST",
            "/dataservice/settings/configuration/wani",
            return_type=str,
            payload=payload,
            **kw,
        )
