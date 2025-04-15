# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CloudTypeParam, TagsResponse

if TYPE_CHECKING:
    from .edge.edge_builder import EdgeBuilder


class TagsBuilder:
    """
    Builds and executes requests for operations under /multicloud/map/tags
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, cloud_type: Optional[CloudTypeParam] = None, **kw) -> TagsResponse:
        """
        Get cloud gateway types for specified cloudType
        GET /dataservice/multicloud/map/tags

        :param cloud_type: Cloud type
        :returns: TagsResponse
        """
        params = {
            "cloudType": cloud_type,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/map/tags", return_type=TagsResponse, params=params, **kw
        )

    @property
    def edge(self) -> EdgeBuilder:
        """
        The edge property
        """
        from .edge.edge_builder import EdgeBuilder

        return EdgeBuilder(self._request_adapter)
