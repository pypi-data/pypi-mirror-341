# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class MetricData:
    # timestamp in seconds
    time: Optional[str] = _field(default=None)
    # count/value for corresponding timestamp
    value: Optional[str] = _field(default=None)


@dataclass
class Neo4JMetricsResponse:
    data: Optional[List[MetricData]] = _field(default=None)
    # limit given in reqeust. By default - 500
    limit: Optional[int] = _field(default=None)
    # Page Number given in request. By default - 1
    page_no: Optional[int] = _field(default=None, metadata={"alias": "pageNo"})
    # Records present on the current page
    records_current_page: Optional[int] = _field(
        default=None, metadata={"alias": "recordsCurrentPage"}
    )
    # Total Pages calculates based on limit and totalRecords values
    total_pages: Optional[int] = _field(default=None, metadata={"alias": "totalPages"})
    # Total count of metrics records ignoring limit
    total_records: Optional[int] = _field(default=None, metadata={"alias": "totalRecords"})
