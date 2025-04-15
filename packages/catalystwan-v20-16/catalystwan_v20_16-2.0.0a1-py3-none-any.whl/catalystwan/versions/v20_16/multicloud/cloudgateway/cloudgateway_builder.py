# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CloudGatewayAdjusted,
    CloudGatewayListResponse,
    CloudGatewayPost,
    Taskid,
    UpdateCgw,
)

if TYPE_CHECKING:
    from .config_group.config_group_builder import ConfigGroupBuilder
    from .gateways.gateways_builder import GatewaysBuilder
    from .nva_security_rules.nva_security_rules_builder import NvaSecurityRulesBuilder
    from .nvas.nvas_builder import NvasBuilder
    from .nvasku.nvasku_builder import NvaskuBuilder
    from .resource.resource_builder import ResourceBuilder
    from .resource_groups.resource_groups_builder import ResourceGroupsBuilder
    from .site.site_builder import SiteBuilder
    from .vhubs.vhubs_builder import VhubsBuilder
    from .vnets_noof_attached.vnets_noof_attached_builder import VnetsNoofAttachedBuilder
    from .vpn_gateways.vpn_gateways_builder import VpnGatewaysBuilder
    from .vwans.vwans_builder import VwansBuilder


class CloudgatewayBuilder:
    """
    Builds and executes requests for operations under /multicloud/cloudgateway
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get_list(
        self,
        cloud_type: Optional[str] = None,
        account_id: Optional[str] = None,
        region: Optional[str] = None,
        cloud_gateway_name: Optional[str] = None,
        connectivity_state: Optional[str] = None,
        **kw,
    ) -> List[CloudGatewayListResponse]:
        """
        Get cloud gateways
        GET /dataservice/multicloud/cloudgateway

        :param cloud_type: Multicloud provider type
        :param account_id: Multicloud account id
        :param region: Multicloud region
        :param cloud_gateway_name: Multicloud cloud gateway name
        :param connectivity_state: Multicloud connectivity state
        :returns: List[CloudGatewayListResponse]
        """
        params = {
            "cloudType": cloud_type,
            "accountId": account_id,
            "region": region,
            "cloudGatewayName": cloud_gateway_name,
            "connectivityState": connectivity_state,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/cloudgateway",
            return_type=List[CloudGatewayListResponse],
            params=params,
            **kw,
        )

    def post(self, payload: CloudGatewayPost, **kw) -> Taskid:
        """
        Create cloud gateway
        POST /dataservice/multicloud/cloudgateway

        :param payload: Payloads for updating Cloud Gateway based on CloudType
        :returns: Taskid
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/multicloud/cloudgateway",
            return_type=Taskid,
            payload=payload,
            **kw,
        )

    def get(self, cloud_gateway_name: str, **kw) -> CloudGatewayAdjusted:
        """
        Get cloud gateway by name
        GET /dataservice/multicloud/cloudgateway/{cloudGatewayName}

        :param cloud_gateway_name: Multicloud cloud gateway name
        :returns: CloudGatewayAdjusted
        """
        params = {
            "cloudGatewayName": cloud_gateway_name,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/cloudgateway/{cloudGatewayName}",
            return_type=CloudGatewayAdjusted,
            params=params,
            **kw,
        )

    def put(self, cloud_gateway_name: str, payload: UpdateCgw, **kw) -> Taskid:
        """
        Update cloud gateway
        PUT /dataservice/multicloud/cloudgateway/{cloudGatewayName}

        :param cloud_gateway_name: Cloud gateway name
        :param payload: Payloads for updating Cloud Gateway based on CloudType
        :returns: Taskid
        """
        params = {
            "cloudGatewayName": cloud_gateway_name,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/multicloud/cloudgateway/{cloudGatewayName}",
            return_type=Taskid,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(
        self, cloud_gateway_name: str, delete_all_resources: Optional[str] = "true", **kw
    ) -> Taskid:
        """
        Delete cloud gateway
        DELETE /dataservice/multicloud/cloudgateway/{cloudGatewayName}

        :param cloud_gateway_name: Multicloud cloud gateway name
        :param delete_all_resources: Delete all resources
        :returns: Taskid
        """
        params = {
            "cloudGatewayName": cloud_gateway_name,
            "deleteAllResources": delete_all_resources,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/multicloud/cloudgateway/{cloudGatewayName}",
            return_type=Taskid,
            params=params,
            **kw,
        )

    @property
    def config_group(self) -> ConfigGroupBuilder:
        """
        The config-group property
        """
        from .config_group.config_group_builder import ConfigGroupBuilder

        return ConfigGroupBuilder(self._request_adapter)

    @property
    def gateways(self) -> GatewaysBuilder:
        """
        The gateways property
        """
        from .gateways.gateways_builder import GatewaysBuilder

        return GatewaysBuilder(self._request_adapter)

    @property
    def nva_security_rules(self) -> NvaSecurityRulesBuilder:
        """
        The nvaSecurityRules property
        """
        from .nva_security_rules.nva_security_rules_builder import NvaSecurityRulesBuilder

        return NvaSecurityRulesBuilder(self._request_adapter)

    @property
    def nvas(self) -> NvasBuilder:
        """
        The nvas property
        """
        from .nvas.nvas_builder import NvasBuilder

        return NvasBuilder(self._request_adapter)

    @property
    def nvasku(self) -> NvaskuBuilder:
        """
        The nvasku property
        """
        from .nvasku.nvasku_builder import NvaskuBuilder

        return NvaskuBuilder(self._request_adapter)

    @property
    def resource(self) -> ResourceBuilder:
        """
        The resource property
        """
        from .resource.resource_builder import ResourceBuilder

        return ResourceBuilder(self._request_adapter)

    @property
    def resource_groups(self) -> ResourceGroupsBuilder:
        """
        The resourceGroups property
        """
        from .resource_groups.resource_groups_builder import ResourceGroupsBuilder

        return ResourceGroupsBuilder(self._request_adapter)

    @property
    def site(self) -> SiteBuilder:
        """
        The site property
        """
        from .site.site_builder import SiteBuilder

        return SiteBuilder(self._request_adapter)

    @property
    def vhubs(self) -> VhubsBuilder:
        """
        The vhubs property
        """
        from .vhubs.vhubs_builder import VhubsBuilder

        return VhubsBuilder(self._request_adapter)

    @property
    def vnets_noof_attached(self) -> VnetsNoofAttachedBuilder:
        """
        The vnetsNoofAttached property
        """
        from .vnets_noof_attached.vnets_noof_attached_builder import VnetsNoofAttachedBuilder

        return VnetsNoofAttachedBuilder(self._request_adapter)

    @property
    def vpn_gateways(self) -> VpnGatewaysBuilder:
        """
        The vpn-gateways property
        """
        from .vpn_gateways.vpn_gateways_builder import VpnGatewaysBuilder

        return VpnGatewaysBuilder(self._request_adapter)

    @property
    def vwans(self) -> VwansBuilder:
        """
        The vwans property
        """
        from .vwans.vwans_builder import VwansBuilder

        return VwansBuilder(self._request_adapter)
