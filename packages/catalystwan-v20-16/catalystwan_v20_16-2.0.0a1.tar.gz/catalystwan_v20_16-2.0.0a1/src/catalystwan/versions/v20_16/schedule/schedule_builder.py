# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .create.create_builder import CreateBuilder
    from .list.list_builder import ListBuilder


class ScheduleBuilder:
    """
    Builds and executes requests for operations under /schedule
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, scheduler_id: str, **kw) -> Any:
        """
        Get a schedule record for backup by scheduler id
        GET /dataservice/schedule/{schedulerId}

        :param scheduler_id: scheduler id
        :returns: Any
        """
        params = {
            "schedulerId": scheduler_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/schedule/{schedulerId}", params=params, **kw
        )

    def delete(self, scheduler_id: str, **kw) -> Any:
        """
        Delete a schedule record for backup in vManage by scheduler id
        DELETE /dataservice/schedule/{schedulerId}

        :param scheduler_id: scheduler id
        :returns: Any
        """
        params = {
            "schedulerId": scheduler_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/schedule/{schedulerId}", params=params, **kw
        )

    @property
    def create(self) -> CreateBuilder:
        """
        The create property
        """
        from .create.create_builder import CreateBuilder

        return CreateBuilder(self._request_adapter)

    @property
    def list(self) -> ListBuilder:
        """
        The list property
        """
        from .list.list_builder import ListBuilder

        return ListBuilder(self._request_adapter)
