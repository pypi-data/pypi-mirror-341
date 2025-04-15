# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional, overload

from catalystwan.abc import RequestAdapterInterface


class StatusBuilder:
    """
    Builds and executes requests for operations under /sdavc/protocol-pack/maintenance/upgrade/status
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @overload
    def get(self, uuid: str, **kw) -> Any:
        """
        Get upgrade status for given Task UUID
        GET /dataservice/sdavc/protocol-pack/maintenance/upgrade/status/{uuid}

        :param uuid: Uuid
        :returns: Any
        """
        ...

    @overload
    def get(self, **kw) -> Any:
        """
        Get active deploy job status
        GET /dataservice/sdavc/protocol-pack/maintenance/upgrade/status

        :returns: Any
        """
        ...

    def get(self, uuid: Optional[str] = None, **kw) -> Any:
        # /dataservice/sdavc/protocol-pack/maintenance/upgrade/status/{uuid}
        if self._request_adapter.param_checker([(uuid, str)], []):
            params = {
                "uuid": uuid,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/sdavc/protocol-pack/maintenance/upgrade/status/{uuid}",
                params=params,
                **kw,
            )
        # /dataservice/sdavc/protocol-pack/maintenance/upgrade/status
        if self._request_adapter.param_checker([], [uuid]):
            return self._request_adapter.request(
                "GET", "/dataservice/sdavc/protocol-pack/maintenance/upgrade/status", **kw
            )
        raise RuntimeError("Provided arguments do not match any signature")
