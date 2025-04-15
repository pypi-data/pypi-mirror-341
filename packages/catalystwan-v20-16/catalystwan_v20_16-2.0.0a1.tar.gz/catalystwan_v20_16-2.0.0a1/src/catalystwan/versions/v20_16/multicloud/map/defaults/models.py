# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

CloudTypeParam = Literal["AWS", "AWS_GOVCLOUD", "AZURE", "AZURE_GOVCLOUD", "GCP"]


@dataclass
class MapDefaults:
    conn: Optional[str] = _field(default=None)
    conn_type: Optional[str] = _field(default=None, metadata={"alias": "connType"})
    dest_type: Optional[str] = _field(default=None, metadata={"alias": "destType"})
    editable: Optional[bool] = _field(default=None)
    src_type: Optional[str] = _field(default=None, metadata={"alias": "srcType"})
