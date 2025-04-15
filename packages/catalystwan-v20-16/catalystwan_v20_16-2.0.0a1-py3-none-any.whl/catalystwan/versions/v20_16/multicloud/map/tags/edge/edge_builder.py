# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CloudTypeParam


class EdgeBuilder:
    """
    Builds and executes requests for operations under /multicloud/map/tags/edge
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        cloud_type: CloudTypeParam,
        account_id: Optional[str] = None,
        resource_group: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get default Interconnect mapping tag values
        GET /dataservice/multicloud/map/tags/edge

        :param cloud_type: Cloud type
        :param account_id: Cloud Account Id
        :param resource_group: Resource Group
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getEdgeMappingTags")
        params = {
            "cloudType": cloud_type,
            "accountId": account_id,
            "resourceGroup": resource_group,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/map/tags/edge", params=params, **kw
        )
