# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import HostVpcTagPost, HostVpcTagPut, HostVpcTagResponse, Taskid

if TYPE_CHECKING:
    from .rebalance_vnets.rebalance_vnets_builder import RebalanceVnetsBuilder


class TagsBuilder:
    """
    Builds and executes requests for operations under /multicloud/hostvpc/tags
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        cloud_type: Optional[str] = None,
        region: Optional[str] = None,
        tag_name: Optional[str] = None,
        **kw,
    ) -> List[HostVpcTagResponse]:
        """
        Get VPC Tags
        GET /dataservice/multicloud/hostvpc/tags

        :param cloud_type: Multicloud provider type
        :param region: Region
        :param tag_name: Tag name
        :returns: List[HostVpcTagResponse]
        """
        params = {
            "cloudType": cloud_type,
            "region": region,
            "tagName": tag_name,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/hostvpc/tags",
            return_type=List[HostVpcTagResponse],
            params=params,
            **kw,
        )

    def put(self, payload: HostVpcTagPut, **kw) -> Taskid:
        """
        Edit VPCs for a Tag
        PUT /dataservice/multicloud/hostvpc/tags

        :param payload: Payload for updating VPCs for a Tag
        :returns: Taskid
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/multicloud/hostvpc/tags", return_type=Taskid, payload=payload, **kw
        )

    def post(self, payload: HostVpcTagPost, **kw) -> Taskid:
        """
        Tag a VPC
        POST /dataservice/multicloud/hostvpc/tags

        :param payload: Payload for tagging a VPC
        :returns: Taskid
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/multicloud/hostvpc/tags",
            return_type=Taskid,
            payload=payload,
            **kw,
        )

    def delete(self, tag_name: str, **kw) -> Taskid:
        """
        Delete a Tag
        DELETE /dataservice/multicloud/hostvpc/tags/{tagName}

        :param tag_name: Tag name
        :returns: Taskid
        """
        params = {
            "tagName": tag_name,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/multicloud/hostvpc/tags/{tagName}",
            return_type=Taskid,
            params=params,
            **kw,
        )

    @property
    def rebalance_vnets(self) -> RebalanceVnetsBuilder:
        """
        The rebalanceVnets property
        """
        from .rebalance_vnets.rebalance_vnets_builder import RebalanceVnetsBuilder

        return RebalanceVnetsBuilder(self._request_adapter)
