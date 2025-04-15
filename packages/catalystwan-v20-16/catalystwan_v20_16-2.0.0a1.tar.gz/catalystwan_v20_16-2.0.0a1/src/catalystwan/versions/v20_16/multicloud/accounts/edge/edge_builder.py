# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Optional, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EdgeTypeParam

if TYPE_CHECKING:
    from .credentials.credentials_builder import CredentialsBuilder


class EdgeBuilder:
    """
    Builds and executes requests for operations under /multicloud/accounts/edge
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw):
        """
        Authenticate edge account credentials
        POST /dataservice/multicloud/accounts/edge

        :param payload: Multicloud edge account info
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "validateEdgeAccountAdd")
        return self._request_adapter.request(
            "POST", "/dataservice/multicloud/accounts/edge", payload=payload, **kw
        )

    def put(self, account_id: str, payload: Any, **kw):
        """
        Update Multicloud edge account
        PUT /dataservice/multicloud/accounts/edge/{accountId}

        :param account_id: Multicloud Edge Account Id
        :param payload: Multicloud edge account info
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "updateEdgeAccount")
        params = {
            "accountId": account_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/multicloud/accounts/edge/{accountId}",
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, account_id: str, **kw):
        """
        Delete edge account
        DELETE /dataservice/multicloud/accounts/edge/{accountId}

        :param account_id: Edge Account Id
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "deleteEdgeAccount")
        params = {
            "accountId": account_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/multicloud/accounts/edge/{accountId}", params=params, **kw
        )

    @overload
    def get(self, *, account_id: str, **kw) -> Any:
        """
        Get edge account by account Id
        GET /dataservice/multicloud/accounts/edge/{accountId}

        :param account_id: Edge Account Id
        :returns: Any
        """
        ...

    @overload
    def get(self, *, edge_type: Optional[EdgeTypeParam] = None, **kw) -> Any:
        """
        Get all Multicloud edge accounts
        GET /dataservice/multicloud/accounts/edge

        :param edge_type: Edge type
        :returns: Any
        """
        ...

    def get(
        self, *, edge_type: Optional[EdgeTypeParam] = None, account_id: Optional[str] = None, **kw
    ) -> Any:
        # /dataservice/multicloud/accounts/edge/{accountId}
        if self._request_adapter.param_checker([(account_id, str)], [edge_type]):
            logging.warning("Operation: %s is deprecated", "getEdgeAccountDetails")
            params = {
                "accountId": account_id,
            }
            return self._request_adapter.request(
                "GET", "/dataservice/multicloud/accounts/edge/{accountId}", params=params, **kw
            )
        # /dataservice/multicloud/accounts/edge
        if self._request_adapter.param_checker([], [account_id]):
            logging.warning("Operation: %s is deprecated", "getEdgeAccounts")
            params = {
                "edgeType": edge_type,
            }
            return self._request_adapter.request(
                "GET", "/dataservice/multicloud/accounts/edge", params=params, **kw
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def credentials(self) -> CredentialsBuilder:
        """
        The credentials property
        """
        from .credentials.credentials_builder import CredentialsBuilder

        return CredentialsBuilder(self._request_adapter)
