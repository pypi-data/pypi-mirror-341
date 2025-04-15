# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class MicrosoftTelemetryBuilder:
    """
    Builds and executes requests for operations under /settings/configuration/microsoftTelemetry
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Retrieve Microsoft telemetry configuration value
        GET /dataservice/settings/configuration/microsoftTelemetry

        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getMicrosoftTelemetryConfiguration")
        return self._request_adapter.request(
            "GET", "/dataservice/settings/configuration/microsoftTelemetry", **kw
        )

    def put(self, payload: str, **kw) -> Any:
        """
        Update Microsoft telemetry configuration setting
        PUT /dataservice/settings/configuration/microsoftTelemetry

        :param payload: Payload
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "editMicrosoftTelemetryConfiguration")
        return self._request_adapter.request(
            "PUT", "/dataservice/settings/configuration/microsoftTelemetry", payload=payload, **kw
        )

    def post(self, payload: str, **kw) -> str:
        """
        Add new Microsoft telemetry configuration
        POST /dataservice/settings/configuration/microsoftTelemetry

        :param payload: Payload
        :returns: str
        """
        logging.warning("Operation: %s is deprecated", "newMicrosoftTelemetryConfiguration")
        return self._request_adapter.request(
            "POST",
            "/dataservice/settings/configuration/microsoftTelemetry",
            return_type=str,
            payload=payload,
            **kw,
        )
