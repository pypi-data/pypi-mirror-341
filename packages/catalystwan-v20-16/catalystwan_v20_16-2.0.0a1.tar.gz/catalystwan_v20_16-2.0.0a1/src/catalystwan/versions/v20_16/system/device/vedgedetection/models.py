# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class VedgeCheckResponseData:
    """
    data field
    """

    v_edge_device_present: Optional[bool] = _field(
        default=None, metadata={"alias": "vEdgeDevicePresent"}
    )


@dataclass
class VedgeCheckResponseHeaderColumnsColor:
    key: Optional[str] = _field(default=None)
    property: Optional[str] = _field(default=None)
    value: Optional[str] = _field(default=None)


@dataclass
class VedgeCheckResponseHeaderColumnsKeyvalue:
    key: Optional[str] = _field(default=None)
    value: Optional[str] = _field(default=None)


@dataclass
class VedgeCheckResponseHeaderColumnsSort:
    direction: Optional[str] = _field(default=None)
    priority: Optional[int] = _field(default=None)


@dataclass
class VedgeCheckResponseHeaderColumns:
    action_column: Optional[bool] = _field(default=None, metadata={"alias": "actionColumn"})
    array_data_type: Optional[str] = _field(default=None, metadata={"alias": "arrayDataType"})
    color: Optional[VedgeCheckResponseHeaderColumnsColor] = _field(default=None)
    color_property: Optional[str] = _field(default=None, metadata={"alias": "colorProperty"})
    data_type: Optional[str] = _field(default=None, metadata={"alias": "dataType"})
    default_property_key: Optional[str] = _field(
        default=None, metadata={"alias": "defaultPropertyKey"}
    )
    default_property_value: Optional[str] = _field(
        default=None, metadata={"alias": "defaultPropertyValue"}
    )
    display: Optional[str] = _field(default=None)
    display_format: Optional[str] = _field(default=None, metadata={"alias": "displayFormat"})
    editable: Optional[bool] = _field(default=None)
    hideable: Optional[bool] = _field(default=None)
    host_value_type: Optional[str] = _field(default=None, metadata={"alias": "hostValueType"})
    icon: Optional[List[VedgeCheckResponseHeaderColumnsKeyvalue]] = _field(default=None)
    icon_property: Optional[str] = _field(default=None, metadata={"alias": "iconProperty"})
    input_format: Optional[str] = _field(default=None, metadata={"alias": "inputFormat"})
    is_left_pinned: Optional[bool] = _field(default=None, metadata={"alias": "isLeftPinned"})
    is_pinned: Optional[bool] = _field(default=None, metadata={"alias": "isPinned"})
    keyvalue: Optional[List[VedgeCheckResponseHeaderColumnsKeyvalue]] = _field(default=None)
    keyvalue_property: Optional[str] = _field(default=None, metadata={"alias": "keyvalueProperty"})
    max_width: Optional[int] = _field(default=None, metadata={"alias": "maxWidth"})
    min_width: Optional[int] = _field(default=None, metadata={"alias": "minWidth"})
    prepended_string: Optional[bool] = _field(default=None, metadata={"alias": "prependedString"})
    property: Optional[str] = _field(default=None)
    sort: Optional[VedgeCheckResponseHeaderColumnsSort] = _field(default=None)
    title: Optional[str] = _field(default=None)
    tool_tip_property: Optional[str] = _field(default=None, metadata={"alias": "toolTipProperty"})
    visible: Optional[bool] = _field(default=None)
    width: Optional[int] = _field(default=None)


@dataclass
class VedgeCheckResponseHeaderFields:
    # dataType field
    data_type: Optional[str] = _field(default=None, metadata={"alias": "dataType"})
    # display field
    display: Optional[str] = _field(default=None)
    # property field
    property: Optional[str] = _field(default=None)


@dataclass
class VedgeCheckResponseHeaderViewKeys:
    unique_key: Optional[List[str]] = _field(default=None, metadata={"alias": "uniqueKey"})


@dataclass
class VedgeCheckResponseHeader:
    """
    header field
    """

    columns: Optional[List[VedgeCheckResponseHeaderColumns]] = _field(default=None)
    fields: Optional[List[VedgeCheckResponseHeaderFields]] = _field(default=None)
    generated_on: Optional[int] = _field(default=None, metadata={"alias": "generatedOn"})
    view_keys: Optional[VedgeCheckResponseHeaderViewKeys] = _field(
        default=None, metadata={"alias": "viewKeys"}
    )


@dataclass
class VedgeCheckResponse:
    # data field
    data: Optional[VedgeCheckResponseData] = _field(default=None)
    # header field
    header: Optional[VedgeCheckResponseHeader] = _field(default=None)
