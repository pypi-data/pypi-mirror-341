# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceModelsResponse


class ModelsBuilder:
    """
    Builds and executes requests for operations under /device/models
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @overload
    def get(self, uuid: str, **kw) -> Any:
        """
        Get device model for the device
        GET /dataservice/device/models/{uuid}

        :param uuid: Device uuid
        :returns: Any
        """
        ...

    @overload
    def get(self, **kw) -> DeviceModelsResponse:
        """
        Get all device models supported by the vManage
        GET /dataservice/device/models

        :returns: DeviceModelsResponse
        """
        ...

    def get(self, uuid: Optional[str] = None, **kw) -> Union[DeviceModelsResponse, Any]:
        # /dataservice/device/models/{uuid}
        if self._request_adapter.param_checker([(uuid, str)], []):
            params = {
                "uuid": uuid,
            }
            return self._request_adapter.request(
                "GET", "/dataservice/device/models/{uuid}", params=params, **kw
            )
        # /dataservice/device/models
        if self._request_adapter.param_checker([], [uuid]):
            return self._request_adapter.request(
                "GET", "/dataservice/device/models", return_type=DeviceModelsResponse, **kw
            )
        raise RuntimeError("Provided arguments do not match any signature")
