# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .async_.async_builder import AsyncBuilder
    from .bulk.bulk_builder import BulkBuilder
    from .delete.delete_builder import DeleteBuilder
    from .switch.switch_builder import SwitchBuilder
    from .vsessionid.vsessionid_builder import VsessionidBuilder
    from .vsmart.vsmart_builder import VsmartBuilder


class TenantBuilder:
    """
    Builds and executes requests for operations under /tenant
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Create a new tenant in Multi-Tenant vManage


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        POST /dataservice/tenant

        :param payload: Tenant model
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "createTenant")
        return self._request_adapter.request("POST", "/dataservice/tenant", payload=payload, **kw)

    @overload
    def get(self, *, tenant_id: str, **kw) -> Any:
        """
        Get a tenant by Id


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/tenant/{tenantId}

        :param tenant_id: Tenant Id
        :returns: Any
        """
        ...

    @overload
    def get(self, *, device_id: Optional[str] = None, **kw) -> List[Any]:
        """
        Lists all the tenants on the vManage


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/tenant

        :param device_id: List all tenants associated with a vSmart or MTEdge
        :returns: List[Any]
        """
        ...

    def get(
        self, *, device_id: Optional[str] = None, tenant_id: Optional[str] = None, **kw
    ) -> Union[List[Any], Any]:
        # /dataservice/tenant/{tenantId}
        if self._request_adapter.param_checker([(tenant_id, str)], [device_id]):
            params = {
                "tenantId": tenant_id,
            }
            return self._request_adapter.request(
                "GET", "/dataservice/tenant/{tenantId}", params=params, **kw
            )
        # /dataservice/tenant
        if self._request_adapter.param_checker([], [tenant_id]):
            params = {
                "deviceId": device_id,
            }
            return self._request_adapter.request(
                "GET", "/dataservice/tenant", return_type=List[Any], params=params, **kw
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @overload
    def put(self, payload: Any, tenant_id: str, **kw) -> Any:
        """
        Update a tenant in Multi-Tenant vManage


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        PUT /dataservice/tenant/{tenantId}

        :param payload: Tenant model
        :param tenant_id: Tenant Id
        :returns: Any
        """
        ...

    @overload
    def put(self, payload: Any, **kw) -> Any:
        """
        Update tenants in Multi-Tenant vManage


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        PUT /dataservice/tenant

        :param payload: Tenant model
        :returns: Any
        """
        ...

    def put(self, payload: Any, tenant_id: Optional[str] = None, **kw) -> Any:
        # /dataservice/tenant/{tenantId}
        if self._request_adapter.param_checker([(payload, Any), (tenant_id, str)], []):
            params = {
                "tenantId": tenant_id,
            }
            return self._request_adapter.request(
                "PUT", "/dataservice/tenant/{tenantId}", params=params, payload=payload, **kw
            )
        # /dataservice/tenant
        if self._request_adapter.param_checker([(payload, Any)], [tenant_id]):
            return self._request_adapter.request(
                "PUT", "/dataservice/tenant", payload=payload, **kw
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def async_(self) -> AsyncBuilder:
        """
        The async property
        """
        from .async_.async_builder import AsyncBuilder

        return AsyncBuilder(self._request_adapter)

    @property
    def bulk(self) -> BulkBuilder:
        """
        The bulk property
        """
        from .bulk.bulk_builder import BulkBuilder

        return BulkBuilder(self._request_adapter)

    @property
    def delete(self) -> DeleteBuilder:
        """
        The delete property
        """
        from .delete.delete_builder import DeleteBuilder

        return DeleteBuilder(self._request_adapter)

    @property
    def switch(self) -> SwitchBuilder:
        """
        The switch property
        """
        from .switch.switch_builder import SwitchBuilder

        return SwitchBuilder(self._request_adapter)

    @property
    def vsessionid(self) -> VsessionidBuilder:
        """
        The vsessionid property
        """
        from .vsessionid.vsessionid_builder import VsessionidBuilder

        return VsessionidBuilder(self._request_adapter)

    @property
    def vsmart(self) -> VsmartBuilder:
        """
        The vsmart property
        """
        from .vsmart.vsmart_builder import VsmartBuilder

        return VsmartBuilder(self._request_adapter)
