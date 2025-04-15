# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface


class CustomappBuilder:
    """
    Builds and executes requests for operations under /template/policy/customapp
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw):
        """
        Create Custom Applications
        POST /dataservice/template/policy/customapp

        :param payload: Create Custom Application
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/template/policy/customapp", payload=payload, **kw
        )

    def put(self, id: str, payload: Any, **kw):
        """
        Update Custom Applications
        PUT /dataservice/template/policy/customapp/{id}

        :param id: Custom Application UUID
        :param payload: Update Custom Application
        :returns: None
        """
        params = {
            "id": id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/template/policy/customapp/{id}",
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, id: str, **kw):
        """
        Delete Custom Application
        DELETE /dataservice/template/policy/customapp/{id}

        :param id: Custom Application UUID
        :returns: None
        """
        params = {
            "id": id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/template/policy/customapp/{id}", params=params, **kw
        )

    @overload
    def get(self, id: str, **kw) -> Any:
        """
        Get a policy custom applications
        GET /dataservice/template/policy/customapp/{id}

        :param id: Id
        :returns: Any
        """
        ...

    @overload
    def get(self, **kw) -> List[Any]:
        """
        Get all policy custom applications
        GET /dataservice/template/policy/customapp

        :returns: List[Any]
        """
        ...

    def get(self, id: Optional[str] = None, **kw) -> Union[List[Any], Any]:
        # /dataservice/template/policy/customapp/{id}
        if self._request_adapter.param_checker([(id, str)], []):
            params = {
                "id": id,
            }
            return self._request_adapter.request(
                "GET", "/dataservice/template/policy/customapp/{id}", params=params, **kw
            )
        # /dataservice/template/policy/customapp
        if self._request_adapter.param_checker([], [id]):
            return self._request_adapter.request(
                "GET", "/dataservice/template/policy/customapp", return_type=List[Any], **kw
            )
        raise RuntimeError("Provided arguments do not match any signature")
