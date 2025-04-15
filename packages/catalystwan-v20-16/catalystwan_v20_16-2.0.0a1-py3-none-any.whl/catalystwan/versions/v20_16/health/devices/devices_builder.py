# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import FeatureTypeParam

if TYPE_CHECKING:
    from .overview.overview_builder import OverviewBuilder


class DevicesBuilder:
    """
    Builds and executes requests for operations under /health/devices
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
        starting_device_id: Optional[str] = None,
        site_id: Optional[str] = None,
        group_id: Optional[str] = None,
        vpn_id: Optional[str] = None,
        reachable: Optional[bool] = None,
        control_status: Optional[str] = None,
        personality: Optional[str] = None,
        health: Optional[str] = None,
        feature_type: Optional[FeatureTypeParam] = None,
        cor_saas_status: Optional[bool] = None,
        include_tenantv_smart: Optional[bool] = None,
        **kw,
    ) -> Any:
        """
        get the devices health properties
        GET /dataservice/health/devices

        :param page: Page Number
        :param page_size: Page Size
        :param sort_by: Sort By Property
        :param sort_order: Sort Order
        :param starting_device_id: Optional device ID to start first page
        :param site_id: Optional site ID to filter devices
        :param group_id: Optional group ID to filter devices
        :param vpn_id: Optional vpn ID to filter devices
        :param reachable: Reachable
        :param control_status: Control status
        :param personality: Personality
        :param health: Health
        :param feature_type: Feature type
        :param cor_saas_status: Cor saas status
        :param include_tenantv_smart: Include vSmarts in tenant view
        :returns: Any
        """
        params = {
            "page": page,
            "pageSize": page_size,
            "sortBy": sort_by,
            "sortOrder": sort_order,
            "startingDeviceId": starting_device_id,
            "siteId": site_id,
            "groupId": group_id,
            "vpnId": vpn_id,
            "reachable": reachable,
            "controlStatus": control_status,
            "personality": personality,
            "health": health,
            "featureType": feature_type,
            "corSaasStatus": cor_saas_status,
            "includeTenantvSmart": include_tenantv_smart,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/health/devices", params=params, **kw
        )

    @property
    def overview(self) -> OverviewBuilder:
        """
        The overview property
        """
        from .overview.overview_builder import OverviewBuilder

        return OverviewBuilder(self._request_adapter)
