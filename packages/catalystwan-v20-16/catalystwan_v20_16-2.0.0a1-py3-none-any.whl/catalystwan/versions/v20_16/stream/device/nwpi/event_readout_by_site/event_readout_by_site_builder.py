# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EventReadoutsResponsePayloadData


class EventReadoutBySiteBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/eventReadoutBySite
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, site_id: str, last_n_hours: int, mode: Optional[str] = None, **kw
    ) -> EventReadoutsResponsePayloadData:
        """
        Get event Readout By Site
        GET /dataservice/stream/device/nwpi/eventReadoutBySite

        :param site_id: site id
        :param last_n_hours: last_n_hours
        :param mode: mode
        :returns: EventReadoutsResponsePayloadData
        """
        logging.warning("Operation: %s is deprecated", "getEventReadoutBySite")
        params = {
            "site_id": site_id,
            "last_n_hours": last_n_hours,
            "mode": mode,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/eventReadoutBySite",
            return_type=EventReadoutsResponsePayloadData,
            params=params,
            **kw,
        )
