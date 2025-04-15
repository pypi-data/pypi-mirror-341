# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ClusterProperties, PutProperties


class ClustersBuilder:
    """
    Builds and executes requests for operations under /app-registry/clusters
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        is_cached: Optional[bool] = True,
        offset: Optional[int] = 0,
        limit: Optional[int] = 0,
        **kw,
    ) -> List[ClusterProperties]:
        """
        Obtain all clusters with associated cloud accounts
        GET /dataservice/app-registry/clusters

        :param is_cached: Is cached
        :param offset: Pagination offset
        :param limit: Pagination limit
        :returns: List[ClusterProperties]
        """
        params = {
            "isCached": is_cached,
            "offset": offset,
            "limit": limit,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/app-registry/clusters",
            return_type=List[ClusterProperties],
            params=params,
            **kw,
        )

    def post(self, **kw):
        """
        Manually upload kubeConfig
        POST /dataservice/app-registry/clusters

        :returns: None
        """
        return self._request_adapter.request("POST", "/dataservice/app-registry/clusters", **kw)

    def put(self, id: str, payload: PutProperties, **kw):
        """
        Edit the discovery status of a cluster
        PUT /dataservice/app-registry/clusters/{id}

        :param id: Id
        :param payload: enable or disable Cluster Discovery Status
        :returns: None
        """
        params = {
            "id": id,
        }
        return self._request_adapter.request(
            "PUT", "/dataservice/app-registry/clusters/{id}", params=params, payload=payload, **kw
        )

    def delete(self, id: str, **kw):
        """
        Delete manually uploaded cluster
        DELETE /dataservice/app-registry/clusters/{id}

        :param id: Id
        :returns: None
        """
        params = {
            "id": id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/app-registry/clusters/{id}", params=params, **kw
        )
