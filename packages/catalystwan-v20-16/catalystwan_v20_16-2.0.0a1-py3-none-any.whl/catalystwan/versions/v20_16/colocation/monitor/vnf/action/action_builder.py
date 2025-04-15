# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceUuid


class ActionBuilder:
    """
    Builds and executes requests for operations under /colocation/monitor/vnf/action
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, vm_name: str, action: str, device_id: Optional[DeviceUuid] = None, **kw):
        """
        To do VNF actions such as start, stop and restart
        POST /dataservice/colocation/monitor/vnf/action

        :param vm_name: Vm name
        :param action: Action
        :param device_id: Device id
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "vnfActions")
        params = {
            "vmName": vm_name,
            "action": action,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/colocation/monitor/vnf/action", params=params, **kw
        )
