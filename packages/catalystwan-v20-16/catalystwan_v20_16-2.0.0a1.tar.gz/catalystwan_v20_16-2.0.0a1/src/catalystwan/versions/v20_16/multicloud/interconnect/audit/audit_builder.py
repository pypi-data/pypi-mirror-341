# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AuditReport


class AuditBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/audit
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        interconnect_type: str,
        connection_type: Optional[str] = None,
        cloud_type: Optional[str] = None,
        device_links: Optional[str] = "false",
        refresh: Optional[str] = "true",
        **kw,
    ) -> AuditReport:
        """
        API to generate audit report for resources.
        GET /dataservice/multicloud/interconnect/audit

        :param interconnect_type: Interconnect provider type
        :param connection_type: Interconnect connectivity type
        :param cloud_type: Cloud provider type
        :param device_links: Interconnect Equinix device link enabled
        :param refresh: Interconnect Audit Refresh Option
        :returns: AuditReport
        """
        params = {
            "interconnect-type": interconnect_type,
            "connection-type": connection_type,
            "cloud-type": cloud_type,
            "device-links": device_links,
            "refresh": refresh,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/audit",
            return_type=AuditReport,
            params=params,
            **kw,
        )
