# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ComponentEventMapping


class GetEventsByComponentBuilder:
    """
    Builds and executes requests for operations under /event/getEventsByComponent
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, query: str, **kw) -> ComponentEventMapping:
        """
        Get event names by component.
        GET /dataservice/event/getEventsByComponent

        :param query: Event component name
        :returns: ComponentEventMapping
        """
        params = {
            "query": query,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/event/getEventsByComponent",
            return_type=ComponentEventMapping,
            params=params,
            **kw,
        )
