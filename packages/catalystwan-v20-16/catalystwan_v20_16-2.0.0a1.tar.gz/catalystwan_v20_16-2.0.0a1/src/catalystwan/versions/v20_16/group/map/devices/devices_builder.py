# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import Vpnid

if TYPE_CHECKING:
    from .links.links_builder import LinksBuilder


class DevicesBuilder:
    """
    Builds and executes requests for operations under /group/map/devices
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, group_id: Optional[str] = None, vpn_id: Optional[List[Vpnid]] = None, **kw):
        """
        Retrieve group devices for map
        GET /dataservice/group/map/devices

        :param group_id: groupId
        :param vpn_id: Vpn id
        :returns: None
        """
        params = {
            "groupId": group_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/group/map/devices", params=params, **kw
        )

    @property
    def links(self) -> LinksBuilder:
        """
        The links property
        """
        from .links.links_builder import LinksBuilder

        return LinksBuilder(self._request_adapter)
