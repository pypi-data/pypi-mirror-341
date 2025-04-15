# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetHsecDevicesPayloadInner

if TYPE_CHECKING:
    from .install.install_builder import InstallBuilder


class DevicesBuilder:
    """
    Builds and executes requests for operations under /hsec/devices
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[GetHsecDevicesPayloadInner]:
        """
        Retrieve list of devices which are valid for fetch of HSEC license
        GET /dataservice/hsec/devices

        :returns: List[GetHsecDevicesPayloadInner]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/hsec/devices", return_type=List[GetHsecDevicesPayloadInner], **kw
        )

    @property
    def install(self) -> InstallBuilder:
        """
        The install property
        """
        from .install.install_builder import InstallBuilder

        return InstallBuilder(self._request_adapter)
