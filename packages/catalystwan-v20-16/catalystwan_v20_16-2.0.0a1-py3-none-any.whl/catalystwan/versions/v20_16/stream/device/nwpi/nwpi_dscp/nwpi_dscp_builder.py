# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import NwpiDscpResponsePayloadInner


class NwpiDscpBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/nwpiDSCP
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[NwpiDscpResponsePayloadInner]:
        """
        Get
        GET /dataservice/stream/device/nwpi/nwpiDSCP

        :returns: List[NwpiDscpResponsePayloadInner]
        """
        logging.warning("Operation: %s is deprecated", "getNwpiDscp")
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/nwpiDSCP",
            return_type=List[NwpiDscpResponsePayloadInner],
            **kw,
        )
