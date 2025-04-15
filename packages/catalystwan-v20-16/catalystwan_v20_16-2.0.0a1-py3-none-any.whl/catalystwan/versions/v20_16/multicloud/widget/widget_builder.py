# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CloudWidget

if TYPE_CHECKING:
    from .edge.edge_builder import EdgeBuilder


class WidgetBuilder:
    """
    Builds and executes requests for operations under /multicloud/widget
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @overload
    def get(self, cloud_type: str, **kw) -> CloudWidget:
        """
        Get cloud widget by cloud type
        GET /dataservice/multicloud/widget/{cloudType}

        :param cloud_type: Cloud type
        :returns: CloudWidget
        """
        ...

    @overload
    def get(self, **kw) -> List[CloudWidget]:
        """
        Get All cloud widgets
        GET /dataservice/multicloud/widget

        :returns: List[CloudWidget]
        """
        ...

    def get(self, cloud_type: Optional[str] = None, **kw) -> Union[List[CloudWidget], CloudWidget]:
        # /dataservice/multicloud/widget/{cloudType}
        if self._request_adapter.param_checker([(cloud_type, str)], []):
            params = {
                "cloudType": cloud_type,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/multicloud/widget/{cloudType}",
                return_type=CloudWidget,
                params=params,
                **kw,
            )
        # /dataservice/multicloud/widget
        if self._request_adapter.param_checker([], [cloud_type]):
            return self._request_adapter.request(
                "GET", "/dataservice/multicloud/widget", return_type=List[CloudWidget], **kw
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def edge(self) -> EdgeBuilder:
        """
        The edge property
        """
        from .edge.edge_builder import EdgeBuilder

        return EdgeBuilder(self._request_adapter)
