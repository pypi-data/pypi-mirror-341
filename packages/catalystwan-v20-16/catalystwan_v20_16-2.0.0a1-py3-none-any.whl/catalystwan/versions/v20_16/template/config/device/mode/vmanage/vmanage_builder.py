# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import TypeParam


class VmanageBuilder:
    """
    Builds and executes requests for operations under /template/config/device/mode/vmanage
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, type_: TypeParam, **kw) -> List[Any]:
        """
        Get list of devices that are allowable for vmanage modes
        GET /dataservice/template/config/device/mode/vmanage

        :param type_: Device type
        :returns: List[Any]
        """
        params = {
            "type": type_,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/template/config/device/mode/vmanage",
            return_type=List[Any],
            params=params,
            **kw,
        )
