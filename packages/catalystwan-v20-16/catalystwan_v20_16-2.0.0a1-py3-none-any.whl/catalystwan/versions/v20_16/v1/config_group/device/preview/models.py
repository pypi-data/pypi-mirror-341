# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional

ValueType = Literal["ARRAY", "FALSE", "NULL", "NUMBER", "OBJECT", "STRING", "TRUE"]


@dataclass
class GetConfigGroupDeviceConfigurationPreviewPostResponse:
    """
    Config Group preview Response schema
    """

    existing_config: str = _field(metadata={"alias": "existingConfig"})
    new_config: str = _field(metadata={"alias": "newConfig"})
    unsupported_parcels: Optional[List[Any]] = _field(
        default=None, metadata={"alias": "unsupportedParcels"}
    )


@dataclass
class GetConfigGroupDeviceConfigurationPreviewPostRequest:
    empty: Optional[bool] = _field(default=None)
    value_type: Optional[ValueType] = _field(default=None, metadata={"alias": "valueType"})
