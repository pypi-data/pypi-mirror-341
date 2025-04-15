# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CreateTopologyGroupPostRequest, EditTopologyGroupPutRequest, TopologyGroup

if TYPE_CHECKING:
    from .device.device_builder import DeviceBuilder


class TopologyGroupBuilder:
    """
    Builds and executes requests for operations under /v1/topology-group
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: CreateTopologyGroupPostRequest, **kw) -> str:
        """
        Create a new Topology Group
        POST /dataservice/v1/topology-group

        :param payload: Topology Group
        :returns: str
        """
        return self._request_adapter.request(
            "POST", "/dataservice/v1/topology-group", return_type=str, payload=payload, **kw
        )

    def put(self, topology_group_id: str, payload: EditTopologyGroupPutRequest, **kw) -> str:
        """
        Edit a Topology Group
        PUT /dataservice/v1/topology-group/{topologyGroupId}

        :param topology_group_id: Topology group id
        :param payload: Topology Group
        :returns: str
        """
        params = {
            "topologyGroupId": topology_group_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/topology-group/{topologyGroupId}",
            return_type=str,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, topology_group_id: str, **kw):
        """
        Delete Topology Group
        DELETE /dataservice/v1/topology-group/{topologyGroupId}

        :param topology_group_id: Topology group id
        :returns: None
        """
        params = {
            "topologyGroupId": topology_group_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/v1/topology-group/{topologyGroupId}", params=params, **kw
        )

    @overload
    def get(self, *, topology_group_id: str, **kw) -> TopologyGroup:
        """
        Get a Topology Group by ID
        GET /dataservice/v1/topology-group/{topologyGroupId}

        :param topology_group_id: Topology group id
        :returns: TopologyGroup
        """
        ...

    @overload
    def get(self, *, solution: Optional[str] = None, **kw) -> List[TopologyGroup]:
        """
        Get a Topology Group by Solution
        GET /dataservice/v1/topology-group

        :param solution: Solution
        :returns: List[TopologyGroup]
        """
        ...

    def get(
        self, *, solution: Optional[str] = None, topology_group_id: Optional[str] = None, **kw
    ) -> Union[List[TopologyGroup], TopologyGroup]:
        # /dataservice/v1/topology-group/{topologyGroupId}
        if self._request_adapter.param_checker([(topology_group_id, str)], [solution]):
            params = {
                "topologyGroupId": topology_group_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/topology-group/{topologyGroupId}",
                return_type=TopologyGroup,
                params=params,
                **kw,
            )
        # /dataservice/v1/topology-group
        if self._request_adapter.param_checker([], [topology_group_id]):
            params = {
                "solution": solution,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/topology-group",
                return_type=List[TopologyGroup],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)
