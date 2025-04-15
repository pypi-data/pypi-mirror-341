# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .cancel.cancel_builder import CancelBuilder
    from .changepartition.changepartition_builder import ChangepartitionBuilder
    from .deactivate.deactivate_builder import DeactivateBuilder
    from .defaultpartition.defaultpartition_builder import DefaultpartitionBuilder
    from .filter.filter_builder import FilterBuilder
    from .firmware.firmware_builder import FirmwareBuilder
    from .firmware_upgrade.firmware_upgrade_builder import FirmwareUpgradeBuilder
    from .image_download.image_download_builder import ImageDownloadBuilder
    from .image_remove.image_remove_builder import ImageRemoveBuilder
    from .install.install_builder import InstallBuilder
    from .list.list_builder import ListBuilder
    from .lxcactivate.lxcactivate_builder import LxcactivateBuilder
    from .lxcdelete.lxcdelete_builder import LxcdeleteBuilder
    from .lxcinstall.lxcinstall_builder import LxcinstallBuilder
    from .lxcreload.lxcreload_builder import LxcreloadBuilder
    from .lxcreset.lxcreset_builder import LxcresetBuilder
    from .lxcupgrade.lxcupgrade_builder import LxcupgradeBuilder
    from .reboot.reboot_builder import RebootBuilder
    from .rediscover.rediscover_builder import RediscoverBuilder
    from .rediscoverall.rediscoverall_builder import RediscoverallBuilder
    from .remote_server.remote_server_builder import RemoteServerBuilder
    from .removepartition.removepartition_builder import RemovepartitionBuilder
    from .security.security_builder import SecurityBuilder
    from .software.software_builder import SoftwareBuilder
    from .startmonitor.startmonitor_builder import StartmonitorBuilder
    from .status.status_builder import StatusBuilder
    from .test.test_builder import TestBuilder
    from .uniquevpnlist.uniquevpnlist_builder import UniquevpnlistBuilder
    from .vnfinstall.vnfinstall_builder import VnfinstallBuilder
    from .vpn.vpn_builder import VpnBuilder
    from .ztp.ztp_builder import ZtpBuilder


class ActionBuilder:
    """
    Builds and executes requests for operations under /device/action
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def cancel(self) -> CancelBuilder:
        """
        The cancel property
        """
        from .cancel.cancel_builder import CancelBuilder

        return CancelBuilder(self._request_adapter)

    @property
    def changepartition(self) -> ChangepartitionBuilder:
        """
        The changepartition property
        """
        from .changepartition.changepartition_builder import ChangepartitionBuilder

        return ChangepartitionBuilder(self._request_adapter)

    @property
    def deactivate(self) -> DeactivateBuilder:
        """
        The deactivate property
        """
        from .deactivate.deactivate_builder import DeactivateBuilder

        return DeactivateBuilder(self._request_adapter)

    @property
    def defaultpartition(self) -> DefaultpartitionBuilder:
        """
        The defaultpartition property
        """
        from .defaultpartition.defaultpartition_builder import DefaultpartitionBuilder

        return DefaultpartitionBuilder(self._request_adapter)

    @property
    def filter(self) -> FilterBuilder:
        """
        The filter property
        """
        from .filter.filter_builder import FilterBuilder

        return FilterBuilder(self._request_adapter)

    @property
    def firmware(self) -> FirmwareBuilder:
        """
        The firmware property
        """
        from .firmware.firmware_builder import FirmwareBuilder

        return FirmwareBuilder(self._request_adapter)

    @property
    def firmware_upgrade(self) -> FirmwareUpgradeBuilder:
        """
        The firmware-upgrade property
        """
        from .firmware_upgrade.firmware_upgrade_builder import FirmwareUpgradeBuilder

        return FirmwareUpgradeBuilder(self._request_adapter)

    @property
    def image_download(self) -> ImageDownloadBuilder:
        """
        The image-download property
        """
        from .image_download.image_download_builder import ImageDownloadBuilder

        return ImageDownloadBuilder(self._request_adapter)

    @property
    def image_remove(self) -> ImageRemoveBuilder:
        """
        The image-remove property
        """
        from .image_remove.image_remove_builder import ImageRemoveBuilder

        return ImageRemoveBuilder(self._request_adapter)

    @property
    def install(self) -> InstallBuilder:
        """
        The install property
        """
        from .install.install_builder import InstallBuilder

        return InstallBuilder(self._request_adapter)

    @property
    def list(self) -> ListBuilder:
        """
        The list property
        """
        from .list.list_builder import ListBuilder

        return ListBuilder(self._request_adapter)

    @property
    def lxcactivate(self) -> LxcactivateBuilder:
        """
        The lxcactivate property
        """
        from .lxcactivate.lxcactivate_builder import LxcactivateBuilder

        return LxcactivateBuilder(self._request_adapter)

    @property
    def lxcdelete(self) -> LxcdeleteBuilder:
        """
        The lxcdelete property
        """
        from .lxcdelete.lxcdelete_builder import LxcdeleteBuilder

        return LxcdeleteBuilder(self._request_adapter)

    @property
    def lxcinstall(self) -> LxcinstallBuilder:
        """
        The lxcinstall property
        """
        from .lxcinstall.lxcinstall_builder import LxcinstallBuilder

        return LxcinstallBuilder(self._request_adapter)

    @property
    def lxcreload(self) -> LxcreloadBuilder:
        """
        The lxcreload property
        """
        from .lxcreload.lxcreload_builder import LxcreloadBuilder

        return LxcreloadBuilder(self._request_adapter)

    @property
    def lxcreset(self) -> LxcresetBuilder:
        """
        The lxcreset property
        """
        from .lxcreset.lxcreset_builder import LxcresetBuilder

        return LxcresetBuilder(self._request_adapter)

    @property
    def lxcupgrade(self) -> LxcupgradeBuilder:
        """
        The lxcupgrade property
        """
        from .lxcupgrade.lxcupgrade_builder import LxcupgradeBuilder

        return LxcupgradeBuilder(self._request_adapter)

    @property
    def reboot(self) -> RebootBuilder:
        """
        The reboot property
        """
        from .reboot.reboot_builder import RebootBuilder

        return RebootBuilder(self._request_adapter)

    @property
    def rediscover(self) -> RediscoverBuilder:
        """
        The rediscover property
        """
        from .rediscover.rediscover_builder import RediscoverBuilder

        return RediscoverBuilder(self._request_adapter)

    @property
    def rediscoverall(self) -> RediscoverallBuilder:
        """
        The rediscoverall property
        """
        from .rediscoverall.rediscoverall_builder import RediscoverallBuilder

        return RediscoverallBuilder(self._request_adapter)

    @property
    def remote_server(self) -> RemoteServerBuilder:
        """
        The remote-server property
        """
        from .remote_server.remote_server_builder import RemoteServerBuilder

        return RemoteServerBuilder(self._request_adapter)

    @property
    def removepartition(self) -> RemovepartitionBuilder:
        """
        The removepartition property
        """
        from .removepartition.removepartition_builder import RemovepartitionBuilder

        return RemovepartitionBuilder(self._request_adapter)

    @property
    def security(self) -> SecurityBuilder:
        """
        The security property
        """
        from .security.security_builder import SecurityBuilder

        return SecurityBuilder(self._request_adapter)

    @property
    def software(self) -> SoftwareBuilder:
        """
        The software property
        """
        from .software.software_builder import SoftwareBuilder

        return SoftwareBuilder(self._request_adapter)

    @property
    def startmonitor(self) -> StartmonitorBuilder:
        """
        The startmonitor property
        """
        from .startmonitor.startmonitor_builder import StartmonitorBuilder

        return StartmonitorBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)

    @property
    def test(self) -> TestBuilder:
        """
        The test property
        """
        from .test.test_builder import TestBuilder

        return TestBuilder(self._request_adapter)

    @property
    def uniquevpnlist(self) -> UniquevpnlistBuilder:
        """
        The uniquevpnlist property
        """
        from .uniquevpnlist.uniquevpnlist_builder import UniquevpnlistBuilder

        return UniquevpnlistBuilder(self._request_adapter)

    @property
    def vnfinstall(self) -> VnfinstallBuilder:
        """
        The vnfinstall property
        """
        from .vnfinstall.vnfinstall_builder import VnfinstallBuilder

        return VnfinstallBuilder(self._request_adapter)

    @property
    def vpn(self) -> VpnBuilder:
        """
        The vpn property
        """
        from .vpn.vpn_builder import VpnBuilder

        return VpnBuilder(self._request_adapter)

    @property
    def ztp(self) -> ZtpBuilder:
        """
        The ztp property
        """
        from .ztp.ztp_builder import ZtpBuilder

        return ZtpBuilder(self._request_adapter)
