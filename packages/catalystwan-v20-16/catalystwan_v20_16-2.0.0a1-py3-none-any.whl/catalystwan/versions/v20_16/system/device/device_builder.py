# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CertificateStates,
    CertificateValidity,
    DeleteDevice,
    DeviceIp,
    DeviceUuid,
    FamilyParam,
    ModelParam,
    TopologyParam,
)

if TYPE_CHECKING:
    from .bootstrap.bootstrap_builder import BootstrapBuilder
    from .claim_devices.claim_devices_builder import ClaimDevicesBuilder
    from .controllers.controllers_builder import ControllersBuilder
    from .decommission.decommission_builder import DecommissionBuilder
    from .devices_without_subject_sudi.devices_without_subject_sudi_builder import (
        DevicesWithoutSubjectSudiBuilder,
    )
    from .fileupload.fileupload_builder import FileuploadBuilder
    from .generate_payg.generate_payg_builder import GeneratePaygBuilder
    from .lifecycle.lifecycle_builder import LifecycleBuilder
    from .management.management_builder import ManagementBuilder
    from .migrate_device.migrate_device_builder import MigrateDeviceBuilder
    from .quickconnect.quickconnect_builder import QuickconnectBuilder
    from .reset.reset_builder import ResetBuilder
    from .rma.rma_builder import RmaBuilder
    from .rootcertchain.rootcertchain_builder import RootcertchainBuilder
    from .selfsignedcert.selfsignedcert_builder import SelfsignedcertBuilder
    from .smartaccount.smartaccount_builder import SmartaccountBuilder
    from .sync.sync_builder import SyncBuilder
    from .tenant.tenant_builder import TenantBuilder
    from .type_.type_builder import TypeBuilder
    from .unclaimed_devices.unclaimed_devices_builder import UnclaimedDevicesBuilder
    from .unlock.unlock_builder import UnlockBuilder
    from .update_device_subject_sudi.update_device_subject_sudi_builder import (
        UpdateDeviceSubjectSudiBuilder,
    )
    from .vedgedetection.vedgedetection_builder import VedgedetectionBuilder
    from .vmanagerootca.vmanagerootca_builder import VmanagerootcaBuilder


class DeviceBuilder:
    """
    Builds and executes requests for operations under /system/device
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw):
        """
        Create new device


        Note: In a multitenant vManage system, this API is only available in the Provider view 123.
        POST /dataservice/system/device

        :param payload: Create device request
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/system/device", payload=payload, **kw
        )

    def get(
        self,
        device_category: str,
        model: Optional[ModelParam] = None,
        state: Optional[List[CertificateStates]] = None,
        uuid: Optional[List[DeviceUuid]] = None,
        device_ip: Optional[List[DeviceIp]] = None,
        validity: Optional[List[CertificateValidity]] = None,
        family: Optional[FamilyParam] = None,
        site_id: Optional[int] = None,
        topology: Optional[TopologyParam] = None,
        tag: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get devices details. When {deviceCategory = controllers}, it returns vEdge sync status, vBond, vManage and vSmart. When {deviceCategory = vedges}, it returns all available vEdge routers
        GET /dataservice/system/device/{deviceCategory}

        :param device_category: Device category
        :param model: Device model
        :param state: List of states
        :param uuid: List of device uuid
        :param device_ip: List of device system IP
        :param validity: List of device validity
        :param family: The platform family to filter for
        :param site_id: The Site Id to filter for
        :param topology: The device topology to filter for
        :param tag: The tag name to filter for
        :returns: Any
        """
        params = {
            "deviceCategory": device_category,
            "model": model,
            "state": state,
            "uuid": uuid,
            "deviceIP": device_ip,
            "validity": validity,
            "family": family,
            "siteId": site_id,
            "topology": topology,
            "tag": tag,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/system/device/{deviceCategory}", params=params, **kw
        )

    def put(self, uuid: str, payload: Any, **kw):
        """
        Edit device
        PUT /dataservice/system/device/{uuid}

        :param uuid: Device UUID
        :param payload: Edit device request
        :returns: None
        """
        params = {
            "uuid": uuid,
        }
        return self._request_adapter.request(
            "PUT", "/dataservice/system/device/{uuid}", params=params, payload=payload, **kw
        )

    def delete(self, uuid: str, **kw) -> DeleteDevice:
        """
        Delete vEdges
        DELETE /dataservice/system/device/{uuid}

        :param uuid: Device uuid
        :returns: DeleteDevice
        """
        params = {
            "uuid": uuid,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/system/device/{uuid}",
            return_type=DeleteDevice,
            params=params,
            **kw,
        )

    @property
    def bootstrap(self) -> BootstrapBuilder:
        """
        The bootstrap property
        """
        from .bootstrap.bootstrap_builder import BootstrapBuilder

        return BootstrapBuilder(self._request_adapter)

    @property
    def claim_devices(self) -> ClaimDevicesBuilder:
        """
        The claimDevices property
        """
        from .claim_devices.claim_devices_builder import ClaimDevicesBuilder

        return ClaimDevicesBuilder(self._request_adapter)

    @property
    def controllers(self) -> ControllersBuilder:
        """
        The controllers property
        """
        from .controllers.controllers_builder import ControllersBuilder

        return ControllersBuilder(self._request_adapter)

    @property
    def decommission(self) -> DecommissionBuilder:
        """
        The decommission property
        """
        from .decommission.decommission_builder import DecommissionBuilder

        return DecommissionBuilder(self._request_adapter)

    @property
    def devices_without_subject_sudi(self) -> DevicesWithoutSubjectSudiBuilder:
        """
        The devicesWithoutSubjectSudi property
        """
        from .devices_without_subject_sudi.devices_without_subject_sudi_builder import (
            DevicesWithoutSubjectSudiBuilder,
        )

        return DevicesWithoutSubjectSudiBuilder(self._request_adapter)

    @property
    def fileupload(self) -> FileuploadBuilder:
        """
        The fileupload property
        """
        from .fileupload.fileupload_builder import FileuploadBuilder

        return FileuploadBuilder(self._request_adapter)

    @property
    def generate_payg(self) -> GeneratePaygBuilder:
        """
        The generate-payg property
        """
        from .generate_payg.generate_payg_builder import GeneratePaygBuilder

        return GeneratePaygBuilder(self._request_adapter)

    @property
    def lifecycle(self) -> LifecycleBuilder:
        """
        The lifecycle property
        """
        from .lifecycle.lifecycle_builder import LifecycleBuilder

        return LifecycleBuilder(self._request_adapter)

    @property
    def management(self) -> ManagementBuilder:
        """
        The management property
        """
        from .management.management_builder import ManagementBuilder

        return ManagementBuilder(self._request_adapter)

    @property
    def migrate_device(self) -> MigrateDeviceBuilder:
        """
        The migrateDevice property
        """
        from .migrate_device.migrate_device_builder import MigrateDeviceBuilder

        return MigrateDeviceBuilder(self._request_adapter)

    @property
    def quickconnect(self) -> QuickconnectBuilder:
        """
        The quickconnect property
        """
        from .quickconnect.quickconnect_builder import QuickconnectBuilder

        return QuickconnectBuilder(self._request_adapter)

    @property
    def reset(self) -> ResetBuilder:
        """
        The reset property
        """
        from .reset.reset_builder import ResetBuilder

        return ResetBuilder(self._request_adapter)

    @property
    def rma(self) -> RmaBuilder:
        """
        The rma property
        """
        from .rma.rma_builder import RmaBuilder

        return RmaBuilder(self._request_adapter)

    @property
    def rootcertchain(self) -> RootcertchainBuilder:
        """
        The rootcertchain property
        """
        from .rootcertchain.rootcertchain_builder import RootcertchainBuilder

        return RootcertchainBuilder(self._request_adapter)

    @property
    def selfsignedcert(self) -> SelfsignedcertBuilder:
        """
        The selfsignedcert property
        """
        from .selfsignedcert.selfsignedcert_builder import SelfsignedcertBuilder

        return SelfsignedcertBuilder(self._request_adapter)

    @property
    def smartaccount(self) -> SmartaccountBuilder:
        """
        The smartaccount property
        """
        from .smartaccount.smartaccount_builder import SmartaccountBuilder

        return SmartaccountBuilder(self._request_adapter)

    @property
    def sync(self) -> SyncBuilder:
        """
        The sync property
        """
        from .sync.sync_builder import SyncBuilder

        return SyncBuilder(self._request_adapter)

    @property
    def tenant(self) -> TenantBuilder:
        """
        The tenant property
        """
        from .tenant.tenant_builder import TenantBuilder

        return TenantBuilder(self._request_adapter)

    @property
    def type_(self) -> TypeBuilder:
        """
        The type property
        """
        from .type_.type_builder import TypeBuilder

        return TypeBuilder(self._request_adapter)

    @property
    def unclaimed_devices(self) -> UnclaimedDevicesBuilder:
        """
        The unclaimedDevices property
        """
        from .unclaimed_devices.unclaimed_devices_builder import UnclaimedDevicesBuilder

        return UnclaimedDevicesBuilder(self._request_adapter)

    @property
    def unlock(self) -> UnlockBuilder:
        """
        The unlock property
        """
        from .unlock.unlock_builder import UnlockBuilder

        return UnlockBuilder(self._request_adapter)

    @property
    def update_device_subject_sudi(self) -> UpdateDeviceSubjectSudiBuilder:
        """
        The updateDeviceSubjectSUDI property
        """
        from .update_device_subject_sudi.update_device_subject_sudi_builder import (
            UpdateDeviceSubjectSudiBuilder,
        )

        return UpdateDeviceSubjectSudiBuilder(self._request_adapter)

    @property
    def vedgedetection(self) -> VedgedetectionBuilder:
        """
        The vedgedetection property
        """
        from .vedgedetection.vedgedetection_builder import VedgedetectionBuilder

        return VedgedetectionBuilder(self._request_adapter)

    @property
    def vmanagerootca(self) -> VmanagerootcaBuilder:
        """
        The vmanagerootca property
        """
        from .vmanagerootca.vmanagerootca_builder import VmanagerootcaBuilder

        return VmanagerootcaBuilder(self._request_adapter)
