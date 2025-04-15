# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import Configurations


class ConfigurationsBuilder:
    """
    Builds and executes requests for operations under /util/logging/configurations
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Configurations:
        """
        List logger configuration
        GET /dataservice/util/logging/configurations

        :returns: Configurations
        """
        return self._request_adapter.request(
            "GET", "/dataservice/util/logging/configurations", return_type=Configurations, **kw
        )
