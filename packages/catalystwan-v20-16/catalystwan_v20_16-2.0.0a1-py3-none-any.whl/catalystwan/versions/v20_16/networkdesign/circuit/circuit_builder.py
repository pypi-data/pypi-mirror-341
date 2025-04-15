# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class CircuitBuilder:
    """
    Builds and executes requests for operations under /networkdesign/circuit
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get network circuits
        GET /dataservice/networkdesign/circuit

        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getCircuits")
        return self._request_adapter.request("GET", "/dataservice/networkdesign/circuit", **kw)

    def post(self, payload: Any, **kw) -> Any:
        """
        Create network circuits
        POST /dataservice/networkdesign/circuit

        :param payload: Network circuit
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "createCircuit")
        return self._request_adapter.request(
            "POST", "/dataservice/networkdesign/circuit", payload=payload, **kw
        )

    def delete(self, id: str, **kw):
        """
        Delete network circuits
        DELETE /dataservice/networkdesign/circuit/{id}

        :param id: Id
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "deleteCircuit")
        params = {
            "id": id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/networkdesign/circuit/{id}", params=params, **kw
        )
