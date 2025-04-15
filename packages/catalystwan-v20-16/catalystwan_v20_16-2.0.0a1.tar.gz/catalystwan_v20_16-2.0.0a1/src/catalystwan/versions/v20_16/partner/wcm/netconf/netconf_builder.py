# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import WcmNetconfConfigRequest, WcmNetconfConfigRes


class NetconfBuilder:
    """
    Builds and executes requests for operations under /partner/wcm/netconf
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, nms_id: str, payload: WcmNetconfConfigRequest, **kw) -> WcmNetconfConfigRes:
        """
        Push device configs
        POST /dataservice/partner/wcm/netconf/{nmsId}

        :param nms_id: Nms id
        :param payload: Netconf configuration
        :returns: WcmNetconfConfigRes
        """
        params = {
            "nmsId": nms_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/partner/wcm/netconf/{nmsId}",
            return_type=WcmNetconfConfigRes,
            params=params,
            payload=payload,
            **kw,
        )
