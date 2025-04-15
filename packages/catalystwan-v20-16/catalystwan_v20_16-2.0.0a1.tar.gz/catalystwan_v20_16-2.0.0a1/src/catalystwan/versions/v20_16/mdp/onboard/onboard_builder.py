# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .status.status_builder import StatusBuilder


class OnboardBuilder:
    """
    Builds and executes requests for operations under /mdp/onboard
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Start MDP onboarding operation
        POST /dataservice/mdp/onboard

        :param payload: Onboard
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/mdp/onboard", payload=payload, **kw
        )

    def put(self, nms_id: str, payload: Any, **kw) -> Any:
        """
        update MDP onboarding document
        PUT /dataservice/mdp/onboard/{nmsId}

        :param nms_id: Nms id
        :param payload: Onboard
        :returns: Any
        """
        params = {
            "nmsId": nms_id,
        }
        return self._request_adapter.request(
            "PUT", "/dataservice/mdp/onboard/{nmsId}", params=params, payload=payload, **kw
        )

    def delete(self, nms_id: str, **kw):
        """
        offboard the mdp application
        DELETE /dataservice/mdp/onboard/{nmsId}

        :param nms_id: Nms id
        :returns: None
        """
        params = {
            "nmsId": nms_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/mdp/onboard/{nmsId}", params=params, **kw
        )

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)
