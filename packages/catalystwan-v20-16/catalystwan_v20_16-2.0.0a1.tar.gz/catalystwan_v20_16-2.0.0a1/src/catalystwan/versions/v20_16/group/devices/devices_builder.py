# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import Vpnid


class DevicesBuilder:
    """
    Builds and executes requests for operations under /group/devices
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        group_id: Optional[str] = None,
        ssh: Optional[bool] = False,
        vpn_id: Optional[List[Vpnid]] = None,
        **kw,
    ) -> List[Any]:
        """
        Retrieve devices in group
        GET /dataservice/group/devices

        :param group_id: groupId
        :param ssh: Ssh
        :param vpn_id: Vpn id
        :returns: List[Any]
        """
        params = {
            "groupId": group_id,
            "ssh": ssh,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/group/devices", return_type=List[Any], params=params, **kw
        )
