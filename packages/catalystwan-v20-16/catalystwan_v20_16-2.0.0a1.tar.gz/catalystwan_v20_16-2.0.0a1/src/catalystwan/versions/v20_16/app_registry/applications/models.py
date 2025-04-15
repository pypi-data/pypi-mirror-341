# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

ValueType = Literal["ARRAY", "FALSE", "NULL", "NUMBER", "OBJECT", "STRING", "TRUE"]


@dataclass
class EditAppDetailsPutRequest:
    value_type: Optional[ValueType] = _field(default=None, metadata={"alias": "valueType"})


@dataclass
class PayloadItems:
    _rid: str
    business_relevance: str
    common_family: str
    common_family_display: str
    common_name: str
    common_name_display: str
    nbar_family: str
    nbar_name: str
    qosmos_family: str
    qosmos_name: str
    traffic_class: str
    uuid: str
