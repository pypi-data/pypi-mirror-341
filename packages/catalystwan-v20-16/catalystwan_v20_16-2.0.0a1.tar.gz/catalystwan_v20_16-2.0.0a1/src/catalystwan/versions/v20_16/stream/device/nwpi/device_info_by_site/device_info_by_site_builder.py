# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceInfoResponsePayloadData


class DeviceInfoBySiteBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/deviceInfoBySite
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, site_id: str, mode: Optional[str] = None, **kw) -> DeviceInfoResponsePayloadData:
        """
        Get device and interface data by site
        GET /dataservice/stream/device/nwpi/deviceInfoBySite

        :param site_id: Site id
        :param mode: mode
        :returns: DeviceInfoResponsePayloadData
        """
        logging.warning("Operation: %s is deprecated", "getDevicesAndInterfacesBySite")
        params = {
            "site_id": site_id,
            "mode": mode,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/deviceInfoBySite",
            return_type=DeviceInfoResponsePayloadData,
            params=params,
            **kw,
        )
