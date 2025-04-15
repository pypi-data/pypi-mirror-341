# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AdminTechCreateReq

if TYPE_CHECKING:
    from .copy.copy_builder import CopyBuilder
    from .delete.delete_builder import DeleteBuilder
    from .download.download_builder import DownloadBuilder
    from .supportedfeatures.supportedfeatures_builder import SupportedfeaturesBuilder


class AdmintechBuilder:
    """
    Builds and executes requests for operations under /device/tools/admintech
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: AdminTechCreateReq, **kw):
        """
        Generate admin tech logs
        POST /dataservice/device/tools/admintech

        :param payload: Admin tech generation request
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/device/tools/admintech", payload=payload, **kw
        )

    def delete_admin_tech_file(self, request_id: str, **kw):
        """
        Delete admin tech logs
        DELETE /dataservice/device/tools/admintech/{requestID}

        :param request_id: Request Id of admin tech generation request
        :returns: None
        """
        params = {
            "requestID": request_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/device/tools/admintech/{requestID}", params=params, **kw
        )

    @property
    def copy(self) -> CopyBuilder:
        """
        The copy property
        """
        from .copy.copy_builder import CopyBuilder

        return CopyBuilder(self._request_adapter)

    @property
    def delete(self) -> DeleteBuilder:
        """
        The delete property
        """
        from .delete.delete_builder import DeleteBuilder

        return DeleteBuilder(self._request_adapter)

    @property
    def download(self) -> DownloadBuilder:
        """
        The download property
        """
        from .download.download_builder import DownloadBuilder

        return DownloadBuilder(self._request_adapter)

    @property
    def supportedfeatures(self) -> SupportedfeaturesBuilder:
        """
        The supportedfeatures property
        """
        from .supportedfeatures.supportedfeatures_builder import SupportedfeaturesBuilder

        return SupportedfeaturesBuilder(self._request_adapter)
