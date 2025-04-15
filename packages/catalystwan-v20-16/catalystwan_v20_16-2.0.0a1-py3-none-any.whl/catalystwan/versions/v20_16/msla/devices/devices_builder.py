# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetDeviceLicensesInner, GetMslaDevicesPayload, ReleaseLicensesRequest


class DevicesBuilder:
    """
    Builds and executes requests for operations under /msla/devices
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, payload: ReleaseLicensesRequest, **kw):
        """
        Release licenses assigned to the devices
        PUT /dataservice/msla/devices

        :param payload: List of devices for unassigning licenses
        :returns: None
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/msla/devices", payload=payload, **kw
        )

    @overload
    def get(self, *, uuid: str, **kw) -> List[GetDeviceLicensesInner]:
        """
        Get licenses associated to device
        GET /dataservice/msla/devices/{uuid}

        :param uuid: Uuid
        :returns: List[GetDeviceLicensesInner]
        """
        ...

    @overload
    def get(self, *, site_id: Optional[str] = None, **kw) -> GetMslaDevicesPayload:
        """
        Retrieve list of devices and their subscription information
        GET /dataservice/msla/devices

        :param site_id: Site id
        :returns: GetMslaDevicesPayload
        """
        ...

    def get(
        self, *, site_id: Optional[str] = None, uuid: Optional[str] = None, **kw
    ) -> Union[GetMslaDevicesPayload, List[GetDeviceLicensesInner]]:
        # /dataservice/msla/devices/{uuid}
        if self._request_adapter.param_checker([(uuid, str)], [site_id]):
            params = {
                "uuid": uuid,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/msla/devices/{uuid}",
                return_type=List[GetDeviceLicensesInner],
                params=params,
                **kw,
            )
        # /dataservice/msla/devices
        if self._request_adapter.param_checker([], [uuid]):
            params = {
                "site-id": site_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/msla/devices",
                return_type=GetMslaDevicesPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
