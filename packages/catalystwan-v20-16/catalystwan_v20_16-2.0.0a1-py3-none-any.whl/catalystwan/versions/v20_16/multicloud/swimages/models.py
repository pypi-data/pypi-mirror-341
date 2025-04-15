# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

CloudTypeParam = Literal["AWS", "AWS_GOVCLOUD", "AZURE", "AZURE_GOVCLOUD", "GCP"]


@dataclass
class SwImagesResponse:
    device_model: Optional[str] = _field(default=None, metadata={"alias": "deviceModel"})
    display_name: Optional[str] = _field(default=None, metadata={"alias": "displayName"})
    is_payg_image: Optional[bool] = _field(default=None, metadata={"alias": "isPaygImage"})
    software_image_id: Optional[str] = _field(default=None, metadata={"alias": "softwareImageId"})
    version: Optional[str] = _field(default=None)
