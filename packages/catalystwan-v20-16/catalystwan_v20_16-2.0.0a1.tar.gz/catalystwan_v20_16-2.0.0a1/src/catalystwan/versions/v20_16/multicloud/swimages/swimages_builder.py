# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CloudTypeParam, SwImagesResponse


class SwimagesBuilder:
    """
    Builds and executes requests for operations under /multicloud/swimages
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
    ) -> List[SwImagesResponse]:
        """
        Get software image list
        GET /dataservice/multicloud/swimages

        :param cloud_type: Cloud type
        :param account_id: Account id
        :param cloud_region: Cloud region
        :returns: List[SwImagesResponse]
        """
        params = {
            "cloudType": cloud_type,
            "accountId": account_id,
            "cloudRegion": cloud_region,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/swimages",
            return_type=List[SwImagesResponse],
            params=params,
            **kw,
        )
