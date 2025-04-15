# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SdaDevicesRes


class DeviceBuilder:
    """
    Builds and executes requests for operations under /partner/dnac/sda/device
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @overload
    def get(self, partner_id: str, uuid: str, **kw) -> SdaDevicesRes:
        """
        Get SDA enabled devices detail
        GET /dataservice/partner/dnac/sda/device/{partnerId}/{uuid}

        :param partner_id: Partner id
        :param uuid: Uuid
        :returns: SdaDevicesRes
        """
        ...

    @overload
    def get(self, partner_id: str, **kw) -> SdaDevicesRes:
        """
        Get SDA enabled devices
        GET /dataservice/partner/dnac/sda/device/{partnerId}

        :param partner_id: Partner id
        :returns: SdaDevicesRes
        """
        ...

    def get(self, partner_id: str, uuid: Optional[str] = None, **kw) -> SdaDevicesRes:
        # /dataservice/partner/dnac/sda/device/{partnerId}/{uuid}
        if self._request_adapter.param_checker([(partner_id, str), (uuid, str)], []):
            params = {
                "partnerId": partner_id,
                "uuid": uuid,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/partner/dnac/sda/device/{partnerId}/{uuid}",
                return_type=SdaDevicesRes,
                params=params,
                **kw,
            )
        # /dataservice/partner/dnac/sda/device/{partnerId}
        if self._request_adapter.param_checker([(partner_id, str)], [uuid]):
            params = {
                "partnerId": partner_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/partner/dnac/sda/device/{partnerId}",
                return_type=SdaDevicesRes,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
