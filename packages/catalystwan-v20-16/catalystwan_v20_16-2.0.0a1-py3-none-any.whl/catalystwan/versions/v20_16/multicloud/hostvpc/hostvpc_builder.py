# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import HostVpcsResponse

if TYPE_CHECKING:
    from .tags.tags_builder import TagsBuilder


class HostvpcBuilder:
    """
    Builds and executes requests for operations under /multicloud/hostvpc
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        cloud_type: str,
        account_ids: Optional[str] = None,
        region: Optional[str] = None,
        untagged: Optional[str] = None,
        **kw,
    ) -> List[HostVpcsResponse]:
        """
        Get all Host VPCs
        GET /dataservice/multicloud/hostvpc

        :param cloud_type: Multicloud provider type
        :param account_ids: Multicloud cloud gateway enabled
        :param region: Region
        :param untagged: Multicloud cloud gateway enabled
        :returns: List[HostVpcsResponse]
        """
        params = {
            "cloudType": cloud_type,
            "accountIds": account_ids,
            "region": region,
            "untagged": untagged,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/hostvpc",
            return_type=List[HostVpcsResponse],
            params=params,
            **kw,
        )

    @property
    def tags(self) -> TagsBuilder:
        """
        The tags property
        """
        from .tags.tags_builder import TagsBuilder

        return TagsBuilder(self._request_adapter)
