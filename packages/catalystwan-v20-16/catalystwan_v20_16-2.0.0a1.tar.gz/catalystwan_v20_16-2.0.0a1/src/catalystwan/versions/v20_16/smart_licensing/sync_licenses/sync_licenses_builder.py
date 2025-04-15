# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import LicenseUplodFile


class SyncLicensesBuilder:
    """
    Builds and executes requests for operations under /smartLicensing/syncLicenses
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: LicenseUplodFile, **kw) -> Any:
        """
        get all licenses for sa/va
        POST /dataservice/smartLicensing/syncLicenses

        :param payload: Partner
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "syncLicenses")
        return self._request_adapter.request(
            "POST", "/dataservice/smartLicensing/syncLicenses", payload=payload, **kw
        )
