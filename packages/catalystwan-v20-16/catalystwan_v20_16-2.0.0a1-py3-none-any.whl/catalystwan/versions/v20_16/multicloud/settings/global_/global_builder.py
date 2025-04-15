# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CloudTypeParam, GlobalSettings, Taskid


class GlobalBuilder:
    """
    Builds and executes requests for operations under /multicloud/settings/global
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, cloud_type: CloudTypeParam, **kw) -> GlobalSettings:
        """
        Get global settings
        GET /dataservice/multicloud/settings/global

        :param cloud_type: Cloud type
        :returns: GlobalSettings
        """
        params = {
            "cloudType": cloud_type,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/settings/global",
            return_type=GlobalSettings,
            params=params,
            **kw,
        )

    def put(self, payload: GlobalSettings, **kw):
        """
        Update global settings
        PUT /dataservice/multicloud/settings/global

        :param payload: Payload for updating Global Settings based on CloudType
        :returns: None
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/multicloud/settings/global", payload=payload, **kw
        )

    def post(self, payload: GlobalSettings, **kw) -> Taskid:
        """
        Add global settings
        POST /dataservice/multicloud/settings/global

        :param payload: Responses for get Global Settings based CloudType
        :returns: Taskid
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/multicloud/settings/global",
            return_type=Taskid,
            payload=payload,
            **kw,
        )
