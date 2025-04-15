# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class DeleteDevicepairBuilder:
    """
    Builds and executes requests for operations under /template/cor/deleteDevicepair
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def delete(
        self,
        accountid: str,
        transitvpcid: str,
        transitvpcname: str,
        cloudregion: str,
        device_pair_id: str,
        cloudtype: Optional[str] = "AWS",
        **kw,
    ) -> Any:
        """
        Remove device pair
        DELETE /dataservice/template/cor/deleteDevicepair

        :param accountid: Account Id
        :param transitvpcid: VPC Id
        :param transitvpcname: VPC Name
        :param cloudregion: Cloud region
        :param cloudtype: Cloud type
        :param device_pair_id: Device pair Id
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "removeDeviceId")
        params = {
            "accountid": accountid,
            "transitvpcid": transitvpcid,
            "transitvpcname": transitvpcname,
            "cloudregion": cloudregion,
            "cloudtype": cloudtype,
            "devicePairId": device_pair_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/template/cor/deleteDevicepair", params=params, **kw
        )
