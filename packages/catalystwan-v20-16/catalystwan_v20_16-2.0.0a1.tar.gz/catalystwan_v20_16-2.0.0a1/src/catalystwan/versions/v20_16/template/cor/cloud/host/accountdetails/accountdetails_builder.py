# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class AccountdetailsBuilder:
    """
    Builds and executes requests for operations under /template/cor/cloud/host/accountdetails
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get cloud host VPC account details
        GET /dataservice/template/cor/cloud/host/accountdetails

        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getCloudHostVpcAccountDetails")
        return self._request_adapter.request(
            "GET", "/dataservice/template/cor/cloud/host/accountdetails", **kw
        )
