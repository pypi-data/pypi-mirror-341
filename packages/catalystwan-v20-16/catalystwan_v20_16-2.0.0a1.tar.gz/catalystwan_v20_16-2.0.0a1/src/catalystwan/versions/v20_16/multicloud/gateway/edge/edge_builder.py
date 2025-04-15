# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EdgeTypeParam, UpdateIcgwPutRequest

if TYPE_CHECKING:
    from .setting.setting_builder import SettingBuilder
    from .types.types_builder import TypesBuilder


class EdgeBuilder:
    """
    Builds and executes requests for operations under /multicloud/gateway/edge
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get_icgws(
        self,
        edge_type: Optional[EdgeTypeParam] = None,
        account_id: Optional[str] = None,
        region: Optional[str] = None,
        region_id: Optional[str] = None,
        resource_state: Optional[str] = None,
        edge_gateway_name: Optional[str] = None,
        billing_account_id: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get Interconnect Gateways
        GET /dataservice/multicloud/gateway/edge

        :param edge_type: Edge type
        :param account_id: Account Id
        :param region: Region
        :param region_id: Region Id
        :param resource_state: Resource State
        :param edge_gateway_name: Edge gateway name
        :param billing_account_id: billing Account Id
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getIcgws")
        params = {
            "edgeType": edge_type,
            "accountId": account_id,
            "region": region,
            "regionId": region_id,
            "resourceState": resource_state,
            "edgeGatewayName": edge_gateway_name,
            "billingAccountId": billing_account_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/gateway/edge", params=params, **kw
        )

    def post(self, payload: Any, **kw) -> Any:
        """
        Create Interconnect Gateway
        POST /dataservice/multicloud/gateway/edge

        :param payload: Interconnect Gateway
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "createIcgw")
        return self._request_adapter.request(
            "POST", "/dataservice/multicloud/gateway/edge", payload=payload, **kw
        )

    def get(self, edge_gateway_name: str, **kw) -> Any:
        """
        Get Interconnect Gateway by name
        GET /dataservice/multicloud/gateway/edge/{edgeGatewayName}

        :param edge_gateway_name: Edge gateway name
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getIcgwDetails")
        params = {
            "edgeGatewayName": edge_gateway_name,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/gateway/edge/{edgeGatewayName}", params=params, **kw
        )

    def put(self, edge_gateway_name: str, payload: UpdateIcgwPutRequest, **kw) -> Any:
        """
        Update Interconnect Gateway
        PUT /dataservice/multicloud/gateway/edge/{edgeGatewayName}

        :param edge_gateway_name: Edge gateway name
        :param payload: Payload
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "updateIcgw")
        params = {
            "edgeGatewayName": edge_gateway_name,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/multicloud/gateway/edge/{edgeGatewayName}",
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, edge_gateway_name: str, **kw) -> Any:
        """
        Delete Interconnect Gateway
        DELETE /dataservice/multicloud/gateway/edge/{edgeGatewayName}

        :param edge_gateway_name: Edge gateway name
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "deleteIcgw")
        params = {
            "edgeGatewayName": edge_gateway_name,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/multicloud/gateway/edge/{edgeGatewayName}", params=params, **kw
        )

    @property
    def setting(self) -> SettingBuilder:
        """
        The setting property
        """
        from .setting.setting_builder import SettingBuilder

        return SettingBuilder(self._request_adapter)

    @property
    def types(self) -> TypesBuilder:
        """
        The types property
        """
        from .types.types_builder import TypesBuilder

        return TypesBuilder(self._request_adapter)
