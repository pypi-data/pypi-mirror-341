# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import Uuid

if TYPE_CHECKING:
    from .disable.disable_builder import DisableBuilder
    from .download.download_builder import DownloadBuilder
    from .renew.renew_builder import RenewBuilder
    from .search.search_builder import SearchBuilder
    from .sessions.sessions_builder import SessionsBuilder
    from .type_.type_builder import TypeBuilder


class LogBuilder:
    """
    Builds and executes requests for operations under /stream/device/log
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, session_id: Uuid, log_id: Optional[int] = -1, **kw):
        """
        Get
        GET /dataservice/stream/device/log/{sessionId}

        :param session_id: Session id
        :param log_id: Log id
        :returns: None
        """
        params = {
            "sessionId": session_id,
            "logId": log_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/stream/device/log/{sessionId}", params=params, **kw
        )

    @overload
    def post(self, payload: str, log_type: str, device_uuid: str, session_id: str, **kw):
        """
        Stream log
        POST /dataservice/stream/device/log/{logType}/{deviceUUID}/{sessionId}

        :param payload: Payload
        :param log_type: Log type
        :param device_uuid: Device uuid
        :param session_id: Session Id
        :returns: None
        """
        ...

    @overload
    def post(self, payload: str, **kw):
        """
        Get session info log
        POST /dataservice/stream/device/log

        :param payload: Payload
        :returns: None
        """
        ...

    def post(
        self,
        payload: str,
        log_type: Optional[str] = None,
        device_uuid: Optional[str] = None,
        session_id: Optional[str] = None,
        **kw,
    ):
        # /dataservice/stream/device/log/{logType}/{deviceUUID}/{sessionId}
        if self._request_adapter.param_checker(
            [(payload, str), (log_type, str), (device_uuid, str), (session_id, str)], []
        ):
            params = {
                "logType": log_type,
                "deviceUUID": device_uuid,
                "sessionId": session_id,
            }
            return self._request_adapter.request(
                "POST",
                "/dataservice/stream/device/log/{logType}/{deviceUUID}/{sessionId}",
                params=params,
                payload=payload,
                **kw,
            )
        # /dataservice/stream/device/log
        if self._request_adapter.param_checker(
            [(payload, str)], [log_type, device_uuid, session_id]
        ):
            return self._request_adapter.request(
                "POST", "/dataservice/stream/device/log", payload=payload, **kw
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def disable(self) -> DisableBuilder:
        """
        The disable property
        """
        from .disable.disable_builder import DisableBuilder

        return DisableBuilder(self._request_adapter)

    @property
    def download(self) -> DownloadBuilder:
        """
        The download property
        """
        from .download.download_builder import DownloadBuilder

        return DownloadBuilder(self._request_adapter)

    @property
    def renew(self) -> RenewBuilder:
        """
        The renew property
        """
        from .renew.renew_builder import RenewBuilder

        return RenewBuilder(self._request_adapter)

    @property
    def search(self) -> SearchBuilder:
        """
        The search property
        """
        from .search.search_builder import SearchBuilder

        return SearchBuilder(self._request_adapter)

    @property
    def sessions(self) -> SessionsBuilder:
        """
        The sessions property
        """
        from .sessions.sessions_builder import SessionsBuilder

        return SessionsBuilder(self._request_adapter)

    @property
    def type_(self) -> TypeBuilder:
        """
        The type property
        """
        from .type_.type_builder import TypeBuilder

        return TypeBuilder(self._request_adapter)
