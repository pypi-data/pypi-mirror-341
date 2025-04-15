# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, List

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .accountid.accountid_builder import AccountidBuilder
    from .acquire_resource_pool.acquire_resource_pool_builder import AcquireResourcePoolBuilder
    from .ami.ami_builder import AmiBuilder
    from .cloud.cloud_builder import CloudBuilder
    from .create_resource_pool.create_resource_pool_builder import CreateResourcePoolBuilder
    from .delete_devicepair.delete_devicepair_builder import DeleteDevicepairBuilder
    from .device.device_builder import DeviceBuilder
    from .devicepair.devicepair_builder import DevicepairBuilder
    from .external_id.external_id_builder import ExternalIdBuilder
    from .get_transit_device_pair_and_host_list.get_transit_device_pair_and_host_list_builder import (
        GetTransitDevicePairAndHostListBuilder,
    )
    from .get_transit_vpn_list.get_transit_vpn_list_builder import GetTransitVpnListBuilder
    from .hostvpc.hostvpc_builder import HostvpcBuilder
    from .map.map_builder import MapBuilder
    from .pem.pem_builder import PemBuilder
    from .scale.scale_builder import ScaleBuilder
    from .transitvpc.transitvpc_builder import TransitvpcBuilder


class CorBuilder:
    """
    Builds and executes requests for operations under /template/cor
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get Cloud On Ramp list
        GET /dataservice/template/cor

        :returns: List[Any]
        """
        logging.warning("Operation: %s is deprecated", "getCORStatus")
        return self._request_adapter.request(
            "GET", "/dataservice/template/cor", return_type=List[Any], **kw
        )

    def post(self, payload: Any, **kw) -> Any:
        """
        Map Host to Transit VPC/VNet
        POST /dataservice/template/cor

        :param payload: Map host to transit VPC request
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "createAndMap")
        return self._request_adapter.request(
            "POST", "/dataservice/template/cor", payload=payload, **kw
        )

    @property
    def accountid(self) -> AccountidBuilder:
        """
        The accountid property
        """
        from .accountid.accountid_builder import AccountidBuilder

        return AccountidBuilder(self._request_adapter)

    @property
    def acquire_resource_pool(self) -> AcquireResourcePoolBuilder:
        """
        The acquireResourcePool property
        """
        from .acquire_resource_pool.acquire_resource_pool_builder import AcquireResourcePoolBuilder

        return AcquireResourcePoolBuilder(self._request_adapter)

    @property
    def ami(self) -> AmiBuilder:
        """
        The ami property
        """
        from .ami.ami_builder import AmiBuilder

        return AmiBuilder(self._request_adapter)

    @property
    def cloud(self) -> CloudBuilder:
        """
        The cloud property
        """
        from .cloud.cloud_builder import CloudBuilder

        return CloudBuilder(self._request_adapter)

    @property
    def create_resource_pool(self) -> CreateResourcePoolBuilder:
        """
        The createResourcePool property
        """
        from .create_resource_pool.create_resource_pool_builder import CreateResourcePoolBuilder

        return CreateResourcePoolBuilder(self._request_adapter)

    @property
    def delete_devicepair(self) -> DeleteDevicepairBuilder:
        """
        The deleteDevicepair property
        """
        from .delete_devicepair.delete_devicepair_builder import DeleteDevicepairBuilder

        return DeleteDevicepairBuilder(self._request_adapter)

    @property
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)

    @property
    def devicepair(self) -> DevicepairBuilder:
        """
        The devicepair property
        """
        from .devicepair.devicepair_builder import DevicepairBuilder

        return DevicepairBuilder(self._request_adapter)

    @property
    def external_id(self) -> ExternalIdBuilder:
        """
        The externalId property
        """
        from .external_id.external_id_builder import ExternalIdBuilder

        return ExternalIdBuilder(self._request_adapter)

    @property
    def get_transit_device_pair_and_host_list(self) -> GetTransitDevicePairAndHostListBuilder:
        """
        The getTransitDevicePairAndHostList property
        """
        from .get_transit_device_pair_and_host_list.get_transit_device_pair_and_host_list_builder import (
            GetTransitDevicePairAndHostListBuilder,
        )

        return GetTransitDevicePairAndHostListBuilder(self._request_adapter)

    @property
    def get_transit_vpn_list(self) -> GetTransitVpnListBuilder:
        """
        The getTransitVpnList property
        """
        from .get_transit_vpn_list.get_transit_vpn_list_builder import GetTransitVpnListBuilder

        return GetTransitVpnListBuilder(self._request_adapter)

    @property
    def hostvpc(self) -> HostvpcBuilder:
        """
        The hostvpc property
        """
        from .hostvpc.hostvpc_builder import HostvpcBuilder

        return HostvpcBuilder(self._request_adapter)

    @property
    def map(self) -> MapBuilder:
        """
        The map property
        """
        from .map.map_builder import MapBuilder

        return MapBuilder(self._request_adapter)

    @property
    def pem(self) -> PemBuilder:
        """
        The pem property
        """
        from .pem.pem_builder import PemBuilder

        return PemBuilder(self._request_adapter)

    @property
    def scale(self) -> ScaleBuilder:
        """
        The scale property
        """
        from .scale.scale_builder import ScaleBuilder

        return ScaleBuilder(self._request_adapter)

    @property
    def transitvpc(self) -> TransitvpcBuilder:
        """
        The transitvpc property
        """
        from .transitvpc.transitvpc_builder import TransitvpcBuilder

        return TransitvpcBuilder(self._request_adapter)
