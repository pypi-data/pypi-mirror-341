# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class GetStatQueryFieldsFieldData:
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})


@dataclass
class GetStatQueryFieldOptions:
    key: str
    value: str
    enable_date_fields: Optional[bool] = _field(
        default=None, metadata={"alias": "enableDateFields"}
    )
    is_selected: Optional[bool] = _field(default=None, metadata={"alias": "isSelected"})
    number: Optional[str] = _field(default=None)


@dataclass
class GetStatQueryFields:
    data_type: str = _field(metadata={"alias": "dataType"})
    is_required: bool = _field(metadata={"alias": "isRequired"})
    multi_select: bool = _field(metadata={"alias": "multiSelect"})
    name: str
    property: str
    field_data: Optional[GetStatQueryFieldsFieldData] = _field(
        default=None, metadata={"alias": "fieldData"}
    )
    options: Optional[List[GetStatQueryFieldOptions]] = _field(default=None)
