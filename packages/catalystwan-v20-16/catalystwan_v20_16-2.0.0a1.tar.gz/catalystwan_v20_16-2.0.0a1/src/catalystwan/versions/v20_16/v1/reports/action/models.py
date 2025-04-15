# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal

ActionParam = Literal["runnow", "start", "stop"]


@dataclass
class UpdateReportTemplateResponse:
    # Report ID
    report_id: str = _field(metadata={"alias": "reportId"})
