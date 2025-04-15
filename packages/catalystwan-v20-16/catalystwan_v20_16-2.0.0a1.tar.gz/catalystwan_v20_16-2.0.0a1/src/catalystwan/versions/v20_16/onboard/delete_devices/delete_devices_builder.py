# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeleteDetails, DeleteResponseInner


class DeleteDevicesBuilder:
    """
    Builds and executes requests for operations under /onboard/delete-devices
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: DeleteDetails, **kw) -> List[DeleteResponseInner]:
        """
        Delete Manual Onboard Device details
        POST /dataservice/onboard/delete-devices

        :param payload: Payload
        :returns: List[DeleteResponseInner]
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/onboard/delete-devices",
            return_type=List[DeleteResponseInner],
            payload=payload,
            **kw,
        )
