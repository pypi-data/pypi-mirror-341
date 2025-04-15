# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class DpiAppResponseData:
    application: Optional[str] = _field(default=None)
    octets: Optional[int] = _field(default=None)


@dataclass
class DpiAppResponseHeaderChart:
    series: Optional[List[str]] = _field(default=None)
    title: Optional[str] = _field(default=None)
    x_axis: Optional[List[str]] = _field(default=None, metadata={"alias": "xAxis"})
    x_axis_label: Optional[str] = _field(default=None, metadata={"alias": "xAxisLabel"})
    y_axis: Optional[List[str]] = _field(default=None, metadata={"alias": "yAxis"})
    y_axis_label: Optional[str] = _field(default=None, metadata={"alias": "yAxisLabel"})


@dataclass
class DpiAppResponseHeaderColumns:
    data_type: Optional[str] = _field(default=None, metadata={"alias": "dataType"})
    hideable: Optional[bool] = _field(default=None)
    property: Optional[str] = _field(default=None)
    title: Optional[str] = _field(default=None)


@dataclass
class DpiAppResponseHeaderFields:
    data_type: Optional[str] = _field(default=None, metadata={"alias": "dataType"})
    property: Optional[str] = _field(default=None)


@dataclass
class DpiAppResponseHeaderViewKeys:
    preference_key: Optional[str] = _field(default=None, metadata={"alias": "preferenceKey"})
    unique_key: Optional[List[str]] = _field(default=None, metadata={"alias": "uniqueKey"})


@dataclass
class DpiAppResponseHeader:
    chart: Optional[DpiAppResponseHeaderChart] = _field(default=None)
    columns: Optional[List[DpiAppResponseHeaderColumns]] = _field(default=None)
    fields: Optional[List[DpiAppResponseHeaderFields]] = _field(default=None)
    generated_on: Optional[int] = _field(default=None, metadata={"alias": "generatedOn"})
    view_keys: Optional[DpiAppResponseHeaderViewKeys] = _field(
        default=None, metadata={"alias": "viewKeys"}
    )


@dataclass
class DpiAppResponse:
    data: Optional[List[DpiAppResponseData]] = _field(default=None)
    header: Optional[DpiAppResponseHeader] = _field(default=None)
