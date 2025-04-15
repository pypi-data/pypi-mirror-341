# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CloudTypeParam, InstanceSizeResponse

if TYPE_CHECKING:
    from .edge.edge_builder import EdgeBuilder


class InstancesizeBuilder:
    """
    Builds and executes requests for operations under /multicloud/instancesize
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        cloud_type: CloudTypeParam,
        account_id: Optional[str] = None,
        cloud_region: Optional[str] = None,
        **kw,
    ) -> List[InstanceSizeResponse]:
        """
        Get Transit VPC supported size
        GET /dataservice/multicloud/instancesize

        :param cloud_type: Cloud type
        :param account_id: Account id
        :param cloud_region: Cloud region
        :returns: List[InstanceSizeResponse]
        """
        params = {
            "cloudType": cloud_type,
            "accountId": account_id,
            "cloudRegion": cloud_region,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/instancesize",
            return_type=List[InstanceSizeResponse],
            params=params,
            **kw,
        )

    @property
    def edge(self) -> EdgeBuilder:
        """
        The edge property
        """
        from .edge.edge_builder import EdgeBuilder

        return EdgeBuilder(self._request_adapter)
