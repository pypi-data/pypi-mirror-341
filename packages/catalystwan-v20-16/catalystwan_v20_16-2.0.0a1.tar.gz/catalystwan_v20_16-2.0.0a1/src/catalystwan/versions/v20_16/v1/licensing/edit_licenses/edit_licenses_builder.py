# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EditLicenseResponse


class EditLicensesBuilder:
    """
    Builds and executes requests for operations under /v1/licensing/edit-licenses
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, uuid: str, **kw) -> EditLicenseResponse:
        """
        Edit licenses associated to a device
        GET /dataservice/v1/licensing/edit-licenses/{uuid}

        :param uuid: Uuid
        :returns: EditLicenseResponse
        """
        params = {
            "uuid": uuid,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/licensing/edit-licenses/{uuid}",
            return_type=EditLicenseResponse,
            params=params,
            **kw,
        )
