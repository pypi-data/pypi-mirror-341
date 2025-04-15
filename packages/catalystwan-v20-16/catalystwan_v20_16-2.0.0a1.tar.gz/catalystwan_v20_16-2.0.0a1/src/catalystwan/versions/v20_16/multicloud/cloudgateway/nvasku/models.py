# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class NvaSkuListResponseScaleValueList:
    instance_count: Optional[int] = _field(default=None, metadata={"alias": "instanceCount"})
    instance_type: Optional[str] = _field(default=None, metadata={"alias": "instanceType"})
    scale_unit: Optional[str] = _field(default=None, metadata={"alias": "scaleUnit"})


@dataclass
class NvaSkuListResponse:
    account_id: Optional[str] = _field(default=None, metadata={"alias": "accountId"})
    account_name: Optional[str] = _field(default=None, metadata={"alias": "accountName"})
    cloud_type: Optional[str] = _field(default=None, metadata={"alias": "cloudType"})
    nva_sku_id: Optional[str] = _field(default=None, metadata={"alias": "nvaSkuId"})
    nva_sku_name: Optional[str] = _field(default=None, metadata={"alias": "nvaSkuName"})
    scale_value_list: Optional[List[NvaSkuListResponseScaleValueList]] = _field(
        default=None, metadata={"alias": "scaleValueList"}
    )
    version_list: Optional[List[str]] = _field(default=None, metadata={"alias": "versionList"})
