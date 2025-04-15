# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class HostvpcBuilder:
    """
    Builds and executes requests for operations under /template/cor/devicepair/hostvpc
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, transit_vpc_id: str, device_pair_id: str, **kw) -> Any:
        """
        Get host VPC details
        GET /dataservice/template/cor/devicepair/hostvpc

        :param transit_vpc_id: Transit VPC Id
        :param device_pair_id: Device pair Id
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getHostVPCs")
        params = {
            "transitVpcId": transit_vpc_id,
            "devicePairId": device_pair_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/template/cor/devicepair/hostvpc", params=params, **kw
        )
