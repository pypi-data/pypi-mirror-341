# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import Image


class ImagesBuilder:
    """
    Builds and executes requests for operations under /device/action/software/images
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, image_type: List[Image], vnf_type: Optional[str] = None, **kw) -> Any:
        """
        Get software images
        GET /dataservice/device/action/software/images

        :param image_type: imageType
        :param vnf_type: vnfType
        :returns: Any
        """
        params = {
            "imageType": image_type,
            "vnfType": vnf_type,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/action/software/images", params=params, **kw
        )
