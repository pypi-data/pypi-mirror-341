# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .autoscale_properties.autoscale_properties_builder import AutoscalePropertiesBuilder
    from .size.size_builder import SizeBuilder


class TransitvpcBuilder:
    """
    Builds and executes requests for operations under /template/cor/transitvpc
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, accountid: str, cloudregion: str, cloudtype: Optional[str] = "AWS", **kw
    ) -> List[Any]:
        """
        Get transit VPC/VNet list
        GET /dataservice/template/cor/transitvpc

        :param accountid: Account Id
        :param cloudregion: Cloud region
        :param cloudtype: Cloud type
        :returns: List[Any]
        """
        logging.warning("Operation: %s is deprecated", "getTransitVPCs")
        params = {
            "accountid": accountid,
            "cloudregion": cloudregion,
            "cloudtype": cloudtype,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/template/cor/transitvpc",
            return_type=List[Any],
            params=params,
            **kw,
        )

    def put(self, payload: Any, **kw) -> Any:
        """
        Update transit VPC/VNet
        PUT /dataservice/template/cor/transitvpc

        :param payload: VPC
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "updateTransitVPC")
        return self._request_adapter.request(
            "PUT", "/dataservice/template/cor/transitvpc", payload=payload, **kw
        )

    def post(self, payload: Any, **kw) -> Any:
        """
        Create transit VPC/VNet
        POST /dataservice/template/cor/transitvpc

        :param payload: VPC
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "addTransitVPC")
        return self._request_adapter.request(
            "POST", "/dataservice/template/cor/transitvpc", payload=payload, **kw
        )

    @property
    def autoscale_properties(self) -> AutoscalePropertiesBuilder:
        """
        The autoscale-properties property
        """
        from .autoscale_properties.autoscale_properties_builder import AutoscalePropertiesBuilder

        return AutoscalePropertiesBuilder(self._request_adapter)

    @property
    def size(self) -> SizeBuilder:
        """
        The size property
        """
        from .size.size_builder import SizeBuilder

        return SizeBuilder(self._request_adapter)
