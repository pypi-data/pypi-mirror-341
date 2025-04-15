# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    DefaultSuccessResponse,
    GetExtendedApplicationResponse,
    SaveExtendedApplicationRequest,
)

if TYPE_CHECKING:
    from .approve.approve_builder import ApproveBuilder
    from .compliance.compliance_builder import ComplianceBuilder


class CloudSourcedBuilder:
    """
    Builds and executes requests for operations under /sdavc/cloud-sourced
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sort_by: Optional[str] = None,
        order_by: Optional[str] = None,
        application_family: Optional[str] = None,
        application_group: Optional[str] = None,
        traffic_class: Optional[str] = None,
        business_relevance: Optional[str] = None,
        status: Optional[str] = None,
        app_name: Optional[str] = None,
        source: Optional[str] = None,
        search_keyword: Optional[str] = None,
        **kw,
    ) -> GetExtendedApplicationResponse:
        """
        returns all cloud sourced application
        GET /dataservice/sdavc/cloud-sourced

        :param offset: Offset
        :param limit: Limit
        :param sort_by: Sort by
        :param order_by: Order by
        :param application_family: Application family
        :param application_group: Application group
        :param traffic_class: Traffic class
        :param business_relevance: Business relevance
        :param status: Status
        :param app_name: App name
        :param source: Source
        :param search_keyword: Search keyword
        :returns: GetExtendedApplicationResponse
        """
        params = {
            "offset": offset,
            "limit": limit,
            "sortBy": sort_by,
            "orderBy": order_by,
            "applicationFamily": application_family,
            "applicationGroup": application_group,
            "trafficClass": traffic_class,
            "businessRelevance": business_relevance,
            "status": status,
            "appName": app_name,
            "source": source,
            "searchKeyword": search_keyword,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/sdavc/cloud-sourced",
            return_type=GetExtendedApplicationResponse,
            params=params,
            **kw,
        )

    def post(self, payload: SaveExtendedApplicationRequest, **kw) -> DefaultSuccessResponse:
        """
        Post
        POST /dataservice/sdavc/cloud-sourced

        :param payload: Payload
        :returns: DefaultSuccessResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/sdavc/cloud-sourced",
            return_type=DefaultSuccessResponse,
            payload=payload,
            **kw,
        )

    @property
    def approve(self) -> ApproveBuilder:
        """
        The approve property
        """
        from .approve.approve_builder import ApproveBuilder

        return ApproveBuilder(self._request_adapter)

    @property
    def compliance(self) -> ComplianceBuilder:
        """
        The compliance property
        """
        from .compliance.compliance_builder import ComplianceBuilder

        return ComplianceBuilder(self._request_adapter)
