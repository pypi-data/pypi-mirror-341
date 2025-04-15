# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class DpiAggregationResponseData:
    count: Optional[int] = _field(default=None)
    family: Optional[str] = _field(default=None)
    octets: Optional[int] = _field(default=None)


@dataclass
class DpiAggregationResponseHeaderColumns:
    data_type: Optional[str] = _field(default=None, metadata={"alias": "dataType"})
    is_display: Optional[bool] = _field(default=None, metadata={"alias": "isDisplay"})
    property: Optional[str] = _field(default=None)
    title: Optional[str] = _field(default=None)


@dataclass
class DpiAggregationResponseHeaderFields:
    data_type: Optional[str] = _field(default=None, metadata={"alias": "dataType"})
    property: Optional[str] = _field(default=None)


@dataclass
class DpiAggregationResponseHeader:
    columns: Optional[List[DpiAggregationResponseHeaderColumns]] = _field(default=None)
    fields: Optional[List[DpiAggregationResponseHeaderFields]] = _field(default=None)
    generated_on: Optional[int] = _field(default=None, metadata={"alias": "generatedOn"})


@dataclass
class DpiAggregationResponse:
    data: Optional[List[DpiAggregationResponseData]] = _field(default=None)
    header: Optional[DpiAggregationResponseHeader] = _field(default=None)
