# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class GetRootCertStatusAllData:
    last_update_time: Optional[str] = _field(default=None, metadata={"alias": "lastUpdateTime"})
    root_cert_md5: Optional[str] = _field(default=None, metadata={"alias": "rootCertMd5"})
    root_cert_status: Optional[str] = _field(default=None, metadata={"alias": "rootCertStatus"})


@dataclass
class GetRootCertStatusAll:
    data: Optional[List[GetRootCertStatusAllData]] = _field(default=None)
