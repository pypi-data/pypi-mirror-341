# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .cancel.cancel_builder import CancelBuilder
    from .clean.clean_builder import CleanBuilder
    from .clear.clear_builder import ClearBuilder
    from .mw.mw_builder import MwBuilder
    from .tasks.tasks_builder import TasksBuilder


class StatusBuilder:
    """
    Builds and executes requests for operations under /device/action/status
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, process_id: str, **kw) -> Any:
        """
        Find status of action
        GET /dataservice/device/action/status/{processId}

        :param process_id: processId
        :returns: Any
        """
        params = {
            "processId": process_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/action/status/{processId}", params=params, **kw
        )

    @property
    def cancel(self) -> CancelBuilder:
        """
        The cancel property
        """
        from .cancel.cancel_builder import CancelBuilder

        return CancelBuilder(self._request_adapter)

    @property
    def clean(self) -> CleanBuilder:
        """
        The clean property
        """
        from .clean.clean_builder import CleanBuilder

        return CleanBuilder(self._request_adapter)

    @property
    def clear(self) -> ClearBuilder:
        """
        The clear property
        """
        from .clear.clear_builder import ClearBuilder

        return ClearBuilder(self._request_adapter)

    @property
    def mw(self) -> MwBuilder:
        """
        The mw property
        """
        from .mw.mw_builder import MwBuilder

        return MwBuilder(self._request_adapter)

    @property
    def tasks(self) -> TasksBuilder:
        """
        The tasks property
        """
        from .tasks.tasks_builder import TasksBuilder

        return TasksBuilder(self._request_adapter)
