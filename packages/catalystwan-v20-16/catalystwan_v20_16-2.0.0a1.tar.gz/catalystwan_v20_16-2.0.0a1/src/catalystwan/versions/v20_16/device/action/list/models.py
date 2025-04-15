# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class GenerateDeviceActionListInner:
    is_cancel_enabled: Optional[bool] = _field(default=None, metadata={"alias": "isCancelEnabled"})
    is_parallel_execution_enabled: Optional[bool] = _field(
        default=None, metadata={"alias": "isParallelExecutionEnabled"}
    )
    name: Optional[str] = _field(default=None)
