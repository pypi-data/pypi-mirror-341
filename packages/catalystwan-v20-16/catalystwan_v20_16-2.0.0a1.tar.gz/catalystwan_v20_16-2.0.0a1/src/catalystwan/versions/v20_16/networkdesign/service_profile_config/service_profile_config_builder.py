# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ServiceProfileConfigBuilder:
    """
    Builds and executes requests for operations under /networkdesign/serviceProfileConfig
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, profile_id: str, device_model: str, **kw) -> Any:
        """
        Get the service profile config for a given device profile id
        GET /dataservice/networkdesign/serviceProfileConfig/{profileId}

        :param profile_id: Device profile Id
        :param device_model: Device model
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getServiceProfileConfig")
        params = {
            "profileId": profile_id,
            "deviceModel": device_model,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/networkdesign/serviceProfileConfig/{profileId}",
            params=params,
            **kw,
        )
