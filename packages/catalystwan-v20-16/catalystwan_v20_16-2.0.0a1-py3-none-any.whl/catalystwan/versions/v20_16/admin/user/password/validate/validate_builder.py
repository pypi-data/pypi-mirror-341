# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ValidateBuilder:
    """
    Builds and executes requests for operations under /admin/user/password/validate
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw):
        """
        Validate user password
        POST /dataservice/admin/user/password/validate

        :param payload: User password
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "validatePassword_1")
        return self._request_adapter.request(
            "POST", "/dataservice/admin/user/password/validate", payload=payload, **kw
        )
