# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceIp


class InterfaceBuilder:
    """
    Builds and executes requests for operations under /colocation/monitor/vnf/interface
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        vnf_name: str,
        device_ip: Optional[DeviceIp] = None,
        device_class: Optional[str] = None,
        **kw,
    ):
        """
        Get interface detail of VNF
        GET /dataservice/colocation/monitor/vnf/interface

        :param vnf_name: Vnf name
        :param device_ip: Device ip
        :param device_class: Device class
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "getVNFInterfaceDetail")
        params = {
            "vnfName": vnf_name,
            "deviceIp": device_ip,
            "deviceClass": device_class,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/colocation/monitor/vnf/interface", params=params, **kw
        )
