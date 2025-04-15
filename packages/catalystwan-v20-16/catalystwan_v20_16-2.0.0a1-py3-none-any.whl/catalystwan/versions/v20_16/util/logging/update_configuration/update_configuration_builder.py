# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import LoggerNameParam


class UpdateConfigurationBuilder:
    """
    Builds and executes requests for operations under /util/logging/updateConfiguration
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        logger_name: LoggerNameParam,
        size_limit: Optional[int] = None,
        reset: Optional[bool] = False,
        **kw,
    ):
        """
        Update logger configuration for rollover size and max file number
        POST /dataservice/util/logging/updateConfiguration

        :param logger_name: Logger Configuration
        :param size_limit: File size, unit is MB, range (16 - 250)
        :param reset: Reset to default
        :returns: None
        """
        params = {
            "loggerName": logger_name,
            "sizeLimit": size_limit,
            "reset": reset,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/util/logging/updateConfiguration", params=params, **kw
        )
