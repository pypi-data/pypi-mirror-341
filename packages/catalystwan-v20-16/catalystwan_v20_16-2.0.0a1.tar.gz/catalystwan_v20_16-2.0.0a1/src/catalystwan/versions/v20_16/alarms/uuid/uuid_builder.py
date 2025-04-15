# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AlarmResponse


class UuidBuilder:
    """
    Builds and executes requests for operations under /alarms/uuid
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, alarm_uuid: str, include_tenants: Optional[bool] = None, **kw) -> AlarmResponse:
        """
        Get alarm details for given UUID
        GET /dataservice/alarms/uuid/{alarm_uuid}

        :param alarm_uuid: Alarm UUID
        :param include_tenants: Specify whether the tenant alarms need to be visible or not from provider view.
        :returns: AlarmResponse
        """
        params = {
            "alarm_uuid": alarm_uuid,
            "includeTenants": include_tenants,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/alarms/uuid/{alarm_uuid}",
            return_type=AlarmResponse,
            params=params,
            **kw,
        )
