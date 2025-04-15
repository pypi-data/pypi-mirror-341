# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class LicenseBuilder:
    """
    Builds and executes requests for operations under /msla/va/License
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, virtual_account_id: Optional[str] = None, license_type: Optional[str] = None, **kw
    ) -> Any:
        """
        Retrieve MSLA subscription/licenses
        GET /dataservice/msla/va/License

        :param virtual_account_id: virtual_account_id
        :param license_type: licenseType
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getSubscriptions")
        params = {
            "virtual_account_id": virtual_account_id,
            "licenseType": license_type,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/msla/va/License", params=params, **kw
        )
