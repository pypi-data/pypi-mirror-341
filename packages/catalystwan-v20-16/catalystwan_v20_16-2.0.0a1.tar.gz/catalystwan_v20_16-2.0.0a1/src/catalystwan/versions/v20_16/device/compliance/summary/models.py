# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class DeviceComplianceCheckListData:
    controller_count: Optional[int] = _field(default=None, metadata={"alias": "controllerCount"})
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})
    v_edge_count: Optional[int] = _field(default=None, metadata={"alias": "vEdgeCount"})


@dataclass
class DeviceComplianceSummaryResponse:
    check_list: Optional[List[DeviceComplianceCheckListData]] = _field(
        default=None, metadata={"alias": "checkList"}
    )
