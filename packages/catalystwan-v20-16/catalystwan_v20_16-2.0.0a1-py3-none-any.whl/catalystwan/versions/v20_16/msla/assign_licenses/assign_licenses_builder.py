# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AssignMslaLicenses


class AssignLicensesBuilder:
    """
    Builds and executes requests for operations under /msla/assignLicenses
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: AssignMslaLicenses, **kw):
        """
        Assign msla licenses to devices
        POST /dataservice/msla/assignLicenses

        :param payload: List of devices for assigning licenses
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/msla/assignLicenses", payload=payload, **kw
        )
