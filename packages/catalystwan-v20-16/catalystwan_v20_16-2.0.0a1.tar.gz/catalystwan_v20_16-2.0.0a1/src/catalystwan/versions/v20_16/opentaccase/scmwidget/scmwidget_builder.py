# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class ScmwidgetBuilder:
    """
    Builds and executes requests for operations under /opentaccase/scmwidget
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Proxy API for SCM Widget
        GET /dataservice/opentaccase/scmwidget/{var}

        :returns: List[Any]
        """
        logging.warning("Operation: %s is deprecated", "getCall")
        return self._request_adapter.request(
            "GET", "/dataservice/opentaccase/scmwidget/{var}", return_type=List[Any], **kw
        )

    def post(self, **kw) -> List[Any]:
        """
        Prxoy API for SCM Widget
        POST /dataservice/opentaccase/scmwidget/{var}

        :returns: List[Any]
        """
        logging.warning("Operation: %s is deprecated", "postCall")
        return self._request_adapter.request(
            "POST", "/dataservice/opentaccase/scmwidget/{var}", return_type=List[Any], **kw
        )

    def delete(self, **kw) -> List[Any]:
        """
        Proxy API for SCM Widget
        DELETE /dataservice/opentaccase/scmwidget/{var}

        :returns: List[Any]
        """
        logging.warning("Operation: %s is deprecated", "deleteCall")
        return self._request_adapter.request(
            "DELETE", "/dataservice/opentaccase/scmwidget/{var}", return_type=List[Any], **kw
        )
