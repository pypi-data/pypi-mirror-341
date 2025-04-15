# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .device.device_builder import DeviceBuilder
    from .monitor.monitor_builder import MonitorBuilder
    from .physical.physical_builder import PhysicalBuilder


class TopologyBuilder:
    """
    Builds and executes requests for operations under /topology
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Create full topology
        GET /dataservice/topology

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/topology", return_type=List[Any], **kw
        )

    @property
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)

    @property
    def monitor(self) -> MonitorBuilder:
        """
        The monitor property
        """
        from .monitor.monitor_builder import MonitorBuilder

        return MonitorBuilder(self._request_adapter)

    @property
    def physical(self) -> PhysicalBuilder:
        """
        The physical property
        """
        from .physical.physical_builder import PhysicalBuilder

        return PhysicalBuilder(self._request_adapter)
