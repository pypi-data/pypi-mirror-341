# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AlarmResponse


class NotviewedBuilder:
    """
    Builds and executes requests for operations under /alarms/notviewed
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, state: Optional[str] = None, **kw) -> AlarmResponse:
        """
        Get alarms which are not acknowledged by the user.
        GET /dataservice/alarms/notviewed

        :param state: Specify the not viewed alarm state to be fetched. Allowed values : ["active", "cleared"]
        :returns: AlarmResponse
        """
        params = {
            "state": state,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/alarms/notviewed", return_type=AlarmResponse, params=params, **kw
        )
