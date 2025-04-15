# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface


class AuthcodeBuilder:
    """
    Builds and executes requests for operations under /opentaccase/authcode
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        code: Optional[str] = None,
        redirect: Optional[str] = None,
        is_refresh_needed: Optional[bool] = None,
        **kw,
    ) -> List[Any]:
        """
        Gets Access Token for SSO Logjn
        GET /dataservice/opentaccase/authcode

        :param code: Code
        :param redirect: Redirect
        :param is_refresh_needed: Is refresh needed
        :returns: List[Any]
        """
        logging.warning("Operation: %s is deprecated", "oauthAccess")
        params = {
            "code": code,
            "redirect": redirect,
            "isRefreshNeeded": is_refresh_needed,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/opentaccase/authcode", return_type=List[Any], params=params, **kw
        )
