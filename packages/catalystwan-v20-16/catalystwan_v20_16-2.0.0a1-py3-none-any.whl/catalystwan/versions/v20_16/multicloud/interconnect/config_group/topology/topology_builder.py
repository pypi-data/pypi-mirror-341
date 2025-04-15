# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InlineResponse20013


class TopologyBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/{interconnect-type}/config-group/{config-group-id}/topology
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, interconnect_type: str, config_group_id: str, **kw) -> InlineResponse20013:
        """
        API to retrieve current Multicloud Interconnect topology for the Config Group.
        GET /dataservice/multicloud/interconnect/{interconnect-type}/config-group/{config-group-id}/topology

        :param interconnect_type: Interconnect provider type
        :param config_group_id: Config Group Id
        :returns: InlineResponse20013
        """
        params = {
            "interconnect-type": interconnect_type,
            "config-group-id": config_group_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/{interconnect-type}/config-group/{config-group-id}/topology",
            return_type=InlineResponse20013,
            params=params,
            **kw,
        )

    def put(self, interconnect_type: str, config_group_id: str, **kw) -> InlineResponse20013:
        """
        API to update current Multicloud Interconnect topology for the Config Group.
        PUT /dataservice/multicloud/interconnect/{interconnect-type}/config-group/{config-group-id}/topology

        :param interconnect_type: Interconnect provider type
        :param config_group_id: Config Group Id
        :returns: InlineResponse20013
        """
        params = {
            "interconnect-type": interconnect_type,
            "config-group-id": config_group_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/multicloud/interconnect/{interconnect-type}/config-group/{config-group-id}/topology",
            return_type=InlineResponse20013,
            params=params,
            **kw,
        )
