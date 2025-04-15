# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional, overload

from catalystwan.abc import RequestAdapterInterface


class ConnectedDevicesBuilder:
    """
    Builds and executes requests for operations under /clusterManagement/connectedDevices
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @overload
    def get(self, vmanage_ip: str, tenant_id: str, **kw) -> List[Any]:
        """
        Get connected device for vManage for a tenant


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/clusterManagement/{tenantId}/connectedDevices/{vmanageIP}

        :param vmanage_ip: vManage IP
        :param tenant_id: Tenant Id
        :returns: List[Any]
        """
        ...

    @overload
    def get(self, vmanage_ip: str, **kw) -> List[Any]:
        """
        Get connected device for vManage


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/clusterManagement/connectedDevices/{vmanageIP}

        :param vmanage_ip: vManage IP
        :returns: List[Any]
        """
        ...

    def get(self, vmanage_ip: str, tenant_id: Optional[str] = None, **kw) -> List[Any]:
        # /dataservice/clusterManagement/{tenantId}/connectedDevices/{vmanageIP}
        if self._request_adapter.param_checker([(vmanage_ip, str), (tenant_id, str)], []):
            params = {
                "vmanageIP": vmanage_ip,
                "tenantId": tenant_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/clusterManagement/{tenantId}/connectedDevices/{vmanageIP}",
                return_type=List[Any],
                params=params,
                **kw,
            )
        # /dataservice/clusterManagement/connectedDevices/{vmanageIP}
        if self._request_adapter.param_checker([(vmanage_ip, str)], [tenant_id]):
            params = {
                "vmanageIP": vmanage_ip,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/clusterManagement/connectedDevices/{vmanageIP}",
                return_type=List[Any],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
