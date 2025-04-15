# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GenerateBootstrapConfigForVedge


class DeviceBuilder:
    """
    Builds and executes requests for operations under /system/device/bootstrap/device
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        uuid: str,
        configtype: str,
        incl_def_root_cert: bool,
        version: Optional[str] = "v1",
        wanif: Optional[str] = None,
        **kw,
    ) -> GenerateBootstrapConfigForVedge:
        """
        Create vEdge device config
        GET /dataservice/system/device/bootstrap/device/{uuid}

        :param uuid: Device UUID
        :param configtype: configtype
        :param incl_def_root_cert: Incl def root cert
        :param version: Version
        :param wanif: wanif
        :returns: GenerateBootstrapConfigForVedge
        """
        params = {
            "uuid": uuid,
            "configtype": configtype,
            "inclDefRootCert": incl_def_root_cert,
            "version": version,
            "wanif": wanif,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/system/device/bootstrap/device/{uuid}",
            return_type=GenerateBootstrapConfigForVedge,
            params=params,
            **kw,
        )
