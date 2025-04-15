# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InlineResponse200


class TopologyBuilder:
    """
    Builds and executes requests for operations under /multicloud/{cloudType}/config-group/{config-group-id}/topology
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, cloud_type: str, config_group_id: str, **kw) -> InlineResponse200:
        """
        API to retrieve current Multicloud MultiCloud topology for the Config Group.
        GET /dataservice/multicloud/{cloudType}/config-group/{config-group-id}/topology

        :param cloud_type: Cloud type
        :param config_group_id: Config group id
        :returns: InlineResponse200
        """
        params = {
            "cloudType": cloud_type,
            "config-group-id": config_group_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/{cloudType}/config-group/{config-group-id}/topology",
            return_type=InlineResponse200,
            params=params,
            **kw,
        )

    def put(self, cloud_type: str, config_group_id: str, **kw) -> InlineResponse200:
        """
        API to update current MultiCloud topology for the Config Group.
        PUT /dataservice/multicloud/{cloudType}/config-group/{config-group-id}/topology

        :param cloud_type: Cloud type
        :param config_group_id: Config group id
        :returns: InlineResponse200
        """
        params = {
            "cloudType": cloud_type,
            "config-group-id": config_group_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/multicloud/{cloudType}/config-group/{config-group-id}/topology",
            return_type=InlineResponse200,
            params=params,
            **kw,
        )
