# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import TemplateTypeParam


class DownloadBuilder:
    """
    Builds and executes requests for operations under /v1/reports/preview/download
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, template_type: Optional[TemplateTypeParam] = None, **kw) -> str:
        """
        Download a report preview file
        GET /dataservice/v1/reports/preview/download

        :param template_type: Template type
        :returns: str
        """
        params = {
            "templateType": template_type,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/v1/reports/preview/download", return_type=str, params=params, **kw
        )
