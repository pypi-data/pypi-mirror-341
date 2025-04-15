# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .attach.attach_builder import AttachBuilder
    from .attached.attached_builder import AttachedBuilder
    from .device.device_builder import DeviceBuilder
    from .diff.diff_builder import DiffBuilder
    from .quick_connect.quick_connect_builder import QuickConnectBuilder
    from .rmalist.rmalist_builder import RmalistBuilder
    from .rmaupdate.rmaupdate_builder import RmaupdateBuilder
    from .running.running_builder import RunningBuilder
    from .vpn.vpn_builder import VpnBuilder


class ConfigBuilder:
    """
    Builds and executes requests for operations under /template/config
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def attach(self) -> AttachBuilder:
        """
        The attach property
        """
        from .attach.attach_builder import AttachBuilder

        return AttachBuilder(self._request_adapter)

    @property
    def attached(self) -> AttachedBuilder:
        """
        The attached property
        """
        from .attached.attached_builder import AttachedBuilder

        return AttachedBuilder(self._request_adapter)

    @property
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)

    @property
    def diff(self) -> DiffBuilder:
        """
        The diff property
        """
        from .diff.diff_builder import DiffBuilder

        return DiffBuilder(self._request_adapter)

    @property
    def quick_connect(self) -> QuickConnectBuilder:
        """
        The quickConnect property
        """
        from .quick_connect.quick_connect_builder import QuickConnectBuilder

        return QuickConnectBuilder(self._request_adapter)

    @property
    def rmalist(self) -> RmalistBuilder:
        """
        The rmalist property
        """
        from .rmalist.rmalist_builder import RmalistBuilder

        return RmalistBuilder(self._request_adapter)

    @property
    def rmaupdate(self) -> RmaupdateBuilder:
        """
        The rmaupdate property
        """
        from .rmaupdate.rmaupdate_builder import RmaupdateBuilder

        return RmaupdateBuilder(self._request_adapter)

    @property
    def running(self) -> RunningBuilder:
        """
        The running property
        """
        from .running.running_builder import RunningBuilder

        return RunningBuilder(self._request_adapter)

    @property
    def vpn(self) -> VpnBuilder:
        """
        The vpn property
        """
        from .vpn.vpn_builder import VpnBuilder

        return VpnBuilder(self._request_adapter)
