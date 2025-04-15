# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class AuditReportAuditReport:
    err_string: Optional[str] = _field(default=None, metadata={"alias": "errString"})
    region: Optional[str] = _field(default=None)
    report_type: Optional[str] = _field(default=None, metadata={"alias": "reportType"})
    resource_name: Optional[str] = _field(default=None, metadata={"alias": "resourceName"})
    status: Optional[str] = _field(default=None)


@dataclass
class AuditReport:
    audit_report: Optional[List[AuditReportAuditReport]] = _field(
        default=None, metadata={"alias": "auditReport"}
    )
    audit_status: Optional[str] = _field(default=None, metadata={"alias": "auditStatus"})
