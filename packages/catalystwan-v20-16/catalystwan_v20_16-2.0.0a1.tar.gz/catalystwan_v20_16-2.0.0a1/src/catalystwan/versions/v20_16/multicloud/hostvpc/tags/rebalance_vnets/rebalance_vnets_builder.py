# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import Taskid


class RebalanceVnetsBuilder:
    """
    Builds and executes requests for operations under /multicloud/hostvpc/tags/rebalanceVnets
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, cloud_type: str, region: str, tag_name: str, **kw) -> Taskid:
        """
        Tag a VPC
        POST /dataservice/multicloud/hostvpc/tags/rebalanceVnets

        :param cloud_type: Multicloud provider type
        :param region: Region
        :param tag_name: Tag name
        :returns: Taskid
        """
        params = {
            "cloudType": cloud_type,
            "region": region,
            "tagName": tag_name,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/multicloud/hostvpc/tags/rebalanceVnets",
            return_type=Taskid,
            params=params,
            **kw,
        )
