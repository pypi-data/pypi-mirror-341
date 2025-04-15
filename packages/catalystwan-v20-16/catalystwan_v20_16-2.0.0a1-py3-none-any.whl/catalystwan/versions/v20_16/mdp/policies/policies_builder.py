# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .mdpconfig.mdpconfig_builder import MdpconfigBuilder


class PoliciesBuilder:
    """
    Builds and executes requests for operations under /mdp/policies
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, nms_id: str, **kw) -> List[Any]:
        """
        Retrieve MDP policies
        GET /dataservice/mdp/policies/{nmsId}

        :param nms_id: Nms id
        :returns: List[Any]
        """
        params = {
            "nmsId": nms_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/mdp/policies/{nmsId}", return_type=List[Any], params=params, **kw
        )

    def put(self, nms_id: str, payload: Any, **kw) -> Any:
        """
        update policy status
        PUT /dataservice/mdp/policies/{nmsId}

        :param nms_id: Nms id
        :param payload: policyList
        :returns: Any
        """
        params = {
            "nmsId": nms_id,
        }
        return self._request_adapter.request(
            "PUT", "/dataservice/mdp/policies/{nmsId}", params=params, payload=payload, **kw
        )

    @property
    def mdpconfig(self) -> MdpconfigBuilder:
        """
        The mdpconfig property
        """
        from .mdpconfig.mdpconfig_builder import MdpconfigBuilder

        return MdpconfigBuilder(self._request_adapter)
