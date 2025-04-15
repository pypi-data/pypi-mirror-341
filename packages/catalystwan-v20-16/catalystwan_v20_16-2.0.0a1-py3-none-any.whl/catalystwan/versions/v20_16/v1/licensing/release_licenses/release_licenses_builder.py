# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ReleaseLicenses


class ReleaseLicensesBuilder:
    """
    Builds and executes requests for operations under /v1/licensing/release-licenses
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, payload: ReleaseLicenses, **kw):
        """
        Release licenses assigned to the devices
        PUT /dataservice/v1/licensing/release-licenses

        :param payload: List of devices for releasing licenses
        :returns: None
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/v1/licensing/release-licenses", payload=payload, **kw
        )
